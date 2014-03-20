import sublime
import os
import subprocess

from .bootstrapper import get_config
from .notifier import log_info, log_error, log_fail
from .thread_progress import ThreadProgress
from .command_thread import CommandThread

_appbuilder_path = []

def run_command(command, on_data=None, on_done=None, show_progress=True, in_progress_message="Loading",
    show_status=True, filter_empty_args=True, no_save=False, **kwargs):
    command = _get_appbuilder_path() + command

    if filter_empty_args:
        command = [arg for arg in command if arg]

    thread = CommandThread(command, on_data, on_done, **kwargs)
    thread.start()

    if show_progress:
        progress = ThreadProgress(thread, in_progress_message, "Success", "Failure")
        progress.run(0)

    if show_status:
        message = kwargs.get('status_message', False) or ' '.join(command)
        sublime.status_message(message)

    return thread

def show_quick_panel(sublime_command, items, on_done):
    window = sublime_command.get_window()
    window.show_quick_panel(items, on_done)

def _get_appbuilder_path():
    global _appbuilder_path
    if not _appbuilder_path:
        if os.name == "nt":
            _appbuilder_path.append(_find_win_node_path())
            _appbuilder_path.append(_find_win_appbuilder_path())
        elif os.name == "posix":
            _appbuilder_path.append(get_config("osx_node_path"))
            _appbuilder_path.append(get_config("osx_appbuilder_path"))

    return _appbuilder_path

def _find_win_node_path():
    paths = _get_paths()
    for path in paths:
        try:
            node_path = os.path.join(path, get_config("win_node_name"))
            proc = subprocess.Popen([node_path])
            proc.terminate()
            return node_path
        except WindowsError:
            pass
    return get_config("win_node_name")

def _find_win_appbuilder_path():
    paths = _get_paths()
    for path in paths:
        try:
            appbuilder_path = os.path.join(path, get_config("win_appbuilder_name"))
            proc = subprocess.Popen([appbuilder_path + ".cmd"])
            proc.terminate()
            if "npm" in path:
                return os.path.join(path, "node_modules", "appbuilder", "bin", get_config("win_appbuilder_name") + ".js")
            else:
                return os.path.join(path, get_config("win_appbuilder_name") + ".js")
        except WindowsError:
            pass
    return get_config("win_appbuilder_name")

def _get_paths():
    return os.environ["PATH"].split(";")

