import sublime
import os
import notifier
import subprocess

from thread_progress import ThreadProgress
from command_thread import CommandThread

_appbuilder_path = []

_DEFAULT_OSX_NODE_PATH = "/usr/local/bin/node"
_DEFAULT_OSX_APPBUILDER_PATH = "/usr/local/bin/appbuilder"
_WIN_NODE_NAME = "node"
_WIN_APPBUILDER_NAME = "appbuilder"

_installed_appbuilder_cli_version = None

def initialize():
    def on_data(data):
        global _installed_appbuilder_cli_version
        if data:
            _installed_appbuilder_cli_version = data

    def on_done(exit_code):
        global _installed_appbuilder_cli_version
        if exit_code == 0:
            notifier.log_info("Telerik AppBuilder has been initialized successfuly")
        else:
            _installed_appbuilder_cli_version = None
            notifier.fail("Cannot load the Telerik AppBuilder package because the Telerik AppBuilder command-line interface is not installed properly on your system.\n" +
                "For a complete list of the system requirements for running the Telerik AppBuilder package, go to:\n" +
                "https://github.com/Icenium/appbuilder-sublime-package#installation")

    run_command(["--version"], on_data, on_done, True, "Checking AppBuilder CLI version")

def has_working_appbuilder_cli():
    global _installed_appbuilder_cli_version
    return bool(_installed_appbuilder_cli_version)

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
            config = sublime.load_settings("AppBuilder.sublime-settings")
            if config.get("node_osx_path"):
                _appbuilder_path.append(config.get("node_osx_path"))
            else:
                _appbuilder_path.append(_DEFAULT_OSX_NODE_PATH)

            if config.get("appbuilder_osx_path"):
                _appbuilder_path.append(config.get("appbuilder_osx_path"))
            else:
                _appbuilder_path.append(_DEFAULT_OSX_APPBUILDER_PATH)

    return _appbuilder_path

def _find_win_node_path():
    paths = _get_paths()
    for path in paths:
        try:
            node_path = os.path.join(path, _WIN_NODE_NAME)
            proc = subprocess.Popen([node_path])
            proc.terminate()
            return node_path
        except WindowsError:
            pass
    return _WIN_NODE_NAME

def _find_win_appbuilder_path():
    paths = _get_paths()
    for path in paths:
        if "npm" in path:
            try:
                appbuilder_path = os.path.join(path, _WIN_APPBUILDER_NAME)
                proc = subprocess.Popen([appbuilder_path + ".cmd"])
                proc.terminate()
                return os.path.join(path, "node_modules", "appbuilder", "bin", _WIN_APPBUILDER_NAME + ".js")
            except WindowsError:
                pass
    return _WIN_APPBUILDER_NAME

def _get_paths():
    return os.environ["PATH"].split(";")

