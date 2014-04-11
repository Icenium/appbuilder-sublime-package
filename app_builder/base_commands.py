import sublime
import sublime_plugin
import os
import abc

from .bootstrapper import has_compatible_working_appbuilder_cli
from .notifier import log_error

class AppBuilderCommand(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def command_name(self):
        pass

    def is_enabled(self):
        return has_compatible_working_appbuilder_cli()

    @abc.abstractmethod
    def active_view(self):
        pass

    @abc.abstractmethod
    def get_file_name(self):
        pass

    @abc.abstractmethod
    def get_relative_file_name(self):
        pass

    @abc.abstractmethod
    def get_working_dir(self):
        pass

    @abc.abstractmethod
    def get_window(self):
        pass

class AppBuilderWindowCommandBase(AppBuilderCommand, sublime_plugin.WindowCommand):
    def active_view(self):
        return self.window.active_view()

    def _active_file_name(self):
        view = self.active_view()
        if view and view.file_name() and len(view.file_name()) > 0:
            return view.file_name()

    def get_file_name(self):
        return ''

    def get_relative_file_name(self):
        return ''

    def get_working_dir(self):
        file_name = self._active_file_name()
        if file_name:
            return os.path.realpath(os.path.dirname(file_name))
        else:
            try:  # handle case with no open folder
                return self.window.folders()[0]
            except IndexError:
                return ''

    def get_window(self):
        return self.window

class AppBuilderTextCommandBase(AppBuilderCommand, sublime_plugin.TextCommand):
    def active_view(self):
        return self.view

    def get_file_name(self):
        return os.path.basename(self.view.file_name())

    def get_relative_file_name(self):
        working_dir = self.get_working_dir()
        file_path = working_dir.replace(working_dir, '')[1:]
        file_name = os.path.join(file_path, self.get_file_name())

        # windows issues
        return file_name.replace('\\', '/')

    def get_working_dir(self):
        return os.path.realpath(os.path.dirname(self.view.file_name()))

    def get_window(self):
        return self.view.window() or sublime.active_window()
