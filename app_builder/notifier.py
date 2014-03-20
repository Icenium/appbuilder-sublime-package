import sublime
import functools

_INFO_LOG_LEVEL_NAME = "info"
_WARNING_LOG_LEVEL_NAME = "warning"
_ERROR_LOG_LEVEL_NAME = "error"
_FAIL_LEVEL_NAME = "fail"

def log_error(message):
    _process_message(message, _ERROR_LOG_LEVEL_NAME)

def log_warning(message):
    _process_message(message, _WARNING_LOG_LEVEL_NAME)

def log_info(message):
    _process_message(message, _INFO_LOG_LEVEL_NAME)

def log_fail(message):
    _process_message(message, _FAIL_LEVEL_NAME)

def _process_message(message, level):
    window = sublime.active_window()
    if window:
        _log(message, level)
    else:
        sublime.set_timeout(functools.partial(_process_message, message, level), 100)

def _log(message, level):
    if level == _INFO_LOG_LEVEL_NAME:
        _log_info(message)
    elif level == _WARNING_LOG_LEVEL_NAME:
        _log_warning(message)
    elif level == _ERROR_LOG_LEVEL_NAME:
        _log_error(message)
    elif level == _FAIL_LEVEL_NAME:
        _log_fail(message)

def _log_error(message):
    _log_info(message)

def _log_warning(message):
    _log_info(message)

def _log_info(message):
    _show_panel()
    print(message)

def _log_fail(message):
    sublime.error_message(message)

def _show_panel():
    window = sublime.active_window()
    if window == None:
        sublime.set_timeout(_show_panel, 100)
    else:
        window.run_command("show_panel", {"panel": "console"})