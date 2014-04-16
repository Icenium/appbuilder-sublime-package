import sublime
import sublime_plugin
import os
import abc

from .bootstrapper import has_compatible_working_appbuilder_cli
from .command_executor import run_command
from .notifier import log_info, log_error

class AppBuilderCommandBase(sublime_plugin.WindowCommand):
    __metaclass__ = abc.ABCMeta

    def active_view(self):
        return self.window.active_view()

    def _active_file_name(self):
        view = self.active_view()
        if view and view.file_name() and len(view.file_name()) > 0:
            return view.file_name()

    def get_file_name(self):
        return ""

    def get_relative_file_name(self):
        return ""

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

    @abc.abstractmethod
    def command_name(self):
        pass

    def is_enabled(self):
        return has_compatible_working_appbuilder_cli()

    def run_command(self, command, show_progress, in_progress_message, success_message, failure_message):
        command_thread = run_command(command, self.on_data, self.on_finished,
            show_progress, in_progress_message, success_message, failure_message)
        return command_thread

    def on_data(self, data):
        log_info(data)

    def on_finished(self, succeded):
        if succeded:
            log_info("%s finished successfully" % \
                (self.command_name))
        else:
            log_info("%s finished unsuccessfully" % \
                (self.command_name))

class RegularAppBuilderCommand(AppBuilderCommandBase):
    _is_running = False

    def is_enabled(self):
        return super(RegularAppBuilderCommand, self).is_enabled() and not RegularAppBuilderCommand._is_running

    def run(self):
        RegularAppBuilderCommand._is_running = True
        self.on_started()

    @abc.abstractmethod
    def on_started(self):
        pass

    def on_finished(self, succeded):
        RegularAppBuilderCommand._is_running = False
        super(RegularAppBuilderCommand, self).on_finished(succeded)

class ToggleAppBuilderCommand(AppBuilderCommandBase):
    __metaclass__ = abc.ABCMeta

    _is_checked = False
    _is_starting = False
    _command_thread = None

    def run(self):
        if ToggleAppBuilderCommand._is_starting:
            return

        ToggleAppBuilderCommand._is_starting = True

        if ToggleAppBuilderCommand._command_thread == None:
            self.on_starting()
        else:
            try:
                ToggleAppBuilderCommand._command_thread.terminate()
            finally:
                ToggleAppBuilderCommand._command_thread = None
                ToggleAppBuilderCommand._is_starting = False
                ToggleAppBuilderCommand._is_checked = False

    def run_command(command):
        ToggleAppBuilderCommand._command_thread = super(RegularAppBuilderCommand, self).run_command(command,
            self.on_data, self.on_finished, show_progress, in_progress_message, success_message, failure_message)

        ToggleAppBuilderCommand._is_checked = True

    def is_checked(self):
        return ToggleAppBuilderCommand._is_checked

    @abc.abstractmethod
    def on_starting(self):
        pass

    def on_started(self):
        ToggleAppBuilderCommand._is_starting = False

    def on_finished(self, succeded):
        ToggleAppBuilderCommand._command_thread = None
        ToggleAppBuilderCommand._is_checked = False
        ToggleAppBuilderCommand._project_in_sync = None
        super(ToggleAppBuilderCommand, self).on_finished(succeded)
