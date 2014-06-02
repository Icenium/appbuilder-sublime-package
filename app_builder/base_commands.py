import sublime
import sublime_plugin
import os
import abc

from .bootstrapper import has_compatible_working_appbuilder_cli
from .command_executor import run_command
from .notifier import log_info, log_error
from .feature_usage_tracking import ensure_feature_usage_tracking_is_set

class AppBuilderCommandBase(sublime_plugin.ApplicationCommand):
    __metaclass__ = abc.ABCMeta

    def active_view(self):
        return self.get_window().active_view()

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
                return self.get_window().folders()[0]
            except IndexError:
                return ''

    def get_window(self):
        return sublime.active_window()

    @abc.abstractmethod
    def command_name(self):
        pass

    def is_enabled(self):
        return has_compatible_working_appbuilder_cli()

    def run_command(self, command, show_progress = False, in_progress_message = "", success_message = "", failure_message = ""):
        self.get_command_thread(command, show_progress, in_progress_message, success_message, failure_message)

    def get_command_thread(self, command, show_progress = False, in_progress_message = "", success_message = "", failure_message = ""):
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
            log_error("%s failed" % \
                (self.command_name))

class RegularAppBuilderCommand(AppBuilderCommandBase):
    def __init__(self):
        super(RegularAppBuilderCommand, self).__init__()
        self._is_running = False

    def is_enabled(self):
        return super(RegularAppBuilderCommand, self).is_enabled() and not self._is_running

    def run(self):
        ensure_feature_usage_tracking_is_set()

        self._is_running = True
        self.on_started()

    @abc.abstractmethod
    def on_started(self):
        pass

    def on_finished(self, succeded):
        self._is_running = False
        super(RegularAppBuilderCommand, self).on_finished(succeded)

class ToggleAppBuilderCommand(AppBuilderCommandBase):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(ToggleAppBuilderCommand, self).__init__()
        self._is_starting = False
        self._is_finishing = False
        self._is_checked = False
        self._command_thread = None

    def run(self):
        ensure_feature_usage_tracking_is_set()

        if self._is_starting or self._is_finishing:
            return

        self._is_starting = True

        if self._command_thread == None:
            self.on_starting()
        else:
            try:
                self._is_finishing = True
                self._command_thread.terminate()
            except:
                self._command_thread = None
                self._is_checked = False
                self._is_finishing = False
            finally:
                self._is_starting = False

    def run_command(self, command):
        self._command_thread = self.get_command_thread(command)
        self._is_checked = True

    def is_checked(self):
        return self._is_checked

    @abc.abstractmethod
    def on_starting(self):
        pass

    def on_started(self):
        self._is_starting = False

    def on_finished(self, succeded):
        self._is_starting = False
        self._command_thread = None
        self._is_checked = False
        self._project_in_sync = None
        self._is_finishing = False
        super(ToggleAppBuilderCommand, self).on_finished(succeded)
