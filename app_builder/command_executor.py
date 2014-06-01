import sublime
import os
import subprocess

from .bootstrapper import get_config
from .notifier import log_info, log_error, log_fail
from .thread_progress import run_progress_indicator
from .command_thread import CommandThread

_appbuilder_path = []

def run_command(command, on_data=None, on_done=None, show_progress=True,
    in_progress_message="Loading", success_message="", failure_message = "",
    show_status=True, filter_empty_args=True, no_save=False, **kwargs):
    appbuilder_path = _get_appbuilder_path()
    if appbuilder_path == None:
        on_done(False)
        return None

    command = appbuilder_path + command

    if filter_empty_args:
        command = [arg for arg in command if arg]

    thread = CommandThread(command, on_data, on_done, **kwargs)
    thread.start()

    if show_progress:
        run_progress_indicator(thread, in_progress_message, success_message, failure_message)

    if show_status:
        message = kwargs.get("status_message", False) or " ".join(command)
        sublime.status_message(message)

    return thread

def show_quick_panel(window, items, on_done):
    window.show_quick_panel(items, on_done)

def _get_appbuilder_path():
    global _appbuilder_path
    if not _appbuilder_path:
        if os.name == "nt":
            _appbuilder_path.append(_find_win_node_path())
            _appbuilder_path.append(_find_win_appbuilder_path())
        elif os.name == "posix":
            osx_node_path = get_config("osx_node_path")
            osx_appbuilder_path = get_config("osx_appbuilder_path")
            if os.path.isfile(osx_node_path) and os.path.isfile(osx_appbuilder_path):
                _appbuilder_path.append(osx_node_path)
                _appbuilder_path.append(osx_appbuilder_path)
            else:
                return None
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
    return os.environ["PATH"].split(os.pathsep)

