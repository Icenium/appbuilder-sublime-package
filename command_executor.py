import sublime
import os

from thread_progress import ThreadProgress
from command_thread import CommandThread
from notifier import Notifier

class AppBuilderCommandExecutor(object):
    _appbuilder_path = []

    DEFAULT_OSX_NODE_PATH = "/usr/local/bin/node"
    DEFAULT_OSX_APPBUILDER_PATH = "/usr/local/bin/appbuilder"
    DEFAULT_WIN_APPBUILDER_PATH = "appbuilder"

    @staticmethod
    def run_command(command, on_data=None, on_done=None, in_progress_message="Loading",
        show_status=True, filter_empty_args=True, no_save=False, **kwargs):
        command = AppBuilderCommandExecutor._get_app_builder_path() + command

        if filter_empty_args:
            command = [arg for arg in command if arg]

        thread = CommandThread(command, on_data, on_done, **kwargs)
        thread.start()

        progress = ThreadProgress(thread, in_progress_message, "Success", "Failure")
        progress.run(0)

        if show_status:
            message = kwargs.get('status_message', False) or ' '.join(command)
            sublime.status_message(message)

        return thread

    @staticmethod
    def show_quick_panel(sublime_command, items, on_done):
        window = sublime_command.get_window()
        window.show_quick_panel(items, on_done)

    @staticmethod
    def _get_app_builder_path():
        if not AppBuilderCommandExecutor._appbuilder_path:
            if os.name == "nt":
                AppBuilderCommandExecutor._appbuilder_path.append(AppBuilderCommandExecutor.DEFAULT_WIN_APPBUILDER_PATH)
            elif os.name == "posix":
                config = sublime.load_settings("AppBuilder.sublime-settings")
                if config.get("node_osx_path"):
                    AppBuilderCommandExecutor._appbuilder_path.append(config.get("node_osx_path"))
                else:
                    AppBuilderCommandExecutor._appbuilder_path.append(DEFAULT_OSX_NODE_PATH)

                if config.get("appbuilder_osx_path"):
                    AppBuilderCommandExecutor._appbuilder_path.append(config.get("appbuilder_osx_path"))
                else:
                    AppBuilderCommandExecutor._appbuilder_path.append(AppBuilderCommandExecutor.DEFAULT_OSX_APPBUILDER_PATH)

        return AppBuilderCommandExecutor._appbuilder_path