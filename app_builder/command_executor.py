import sublime
import os
import subprocess
import platform

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
    command += ["--analyticsClient", "Sublime"]

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

def check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.
 
    Backported from Python 2.7 as it's implemented as pure python on stdlib.
 
    >>> check_output(['/usr/bin/python', '--version'])
    Python 2.6.2
    """
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
            error = subprocess.CalledProcessError(retcode, cmd)
            error.output = output
            raise error
    return output

def _get_appbuilder_path():
    global _appbuilder_path
    if not _appbuilder_path:
        if platform.system() == "Windows":
            _appbuilder_path.append(_find_win_node_path())
            _appbuilder_path.append(_find_win_appbuilder_path())
        elif platform.system() == "Darwin":
            osx_node_path = get_config("osx_node_path")
            osx_appbuilder_path = get_config("osx_appbuilder_path")
            if os.path.isfile(osx_node_path) and os.path.isfile(osx_appbuilder_path):
                _appbuilder_path.append(osx_node_path)
                _appbuilder_path.append(osx_appbuilder_path)
            else:
                return None
        elif platform.system() == "Linux":
            linux_node_path = get_config("linux_node_path")
            linux_appbuilder_path = get_config("linux_appbuilder_path")

            if linux_node_path == "":
                linux_node_path_raw = check_output(['/bin/bash', '-i', '-c', "which node"]) # returns byte string
                linux_node_path = str(linux_node_path_raw.decode("utf-8")).strip()

            if linux_appbuilder_path == "":
                linux_appbuilder_path_raw = check_output(['/bin/bash', '-i', '-c', "which appbuilder"]) # returns byte string
                linux_appbuilder_path = str(linux_appbuilder_path_raw.decode("utf-8")).strip()

            if os.path.isfile(linux_node_path) and os.path.isfile(linux_appbuilder_path):
                _appbuilder_path.append(linux_node_path)
                _appbuilder_path.append(linux_appbuilder_path)
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

