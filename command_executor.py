import sublime

from thread_progress import ThreadProgress
from command_thread import CommandThread
from notifier import Notifier

class AppBuilderCommandExecutor(object):
    APP_BUILDER = "appbuilder"

    @staticmethod
    def run_command(command, on_data=None, on_done=None, in_progress_message="Loading",
        show_status=True, filter_empty_args=True, no_save=False, **kwargs):
        command.insert(0, AppBuilderCommandExecutor.APP_BUILDER)

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