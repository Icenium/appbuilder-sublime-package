import sublime
import json

from .command_executor import run_command
from .notifier import log_info

_usage_reporting_enabled = None

def ensure_usage_reporting_is_set(callback=None):
    if _usage_reporting_enabled != None:
        executeCallback(callback)
        return

    def on_data(data):
        global _usage_reporting_enabled
        if _usage_reporting_enabled == None:
            try:
                parsed_data = json.loads(data)
                _usage_reporting_enabled = parsed_data["enabled"]
            except ValueError: # includes simplejson.decoder.JSONDecodeError
                pass

    def on_done(succeeded):
        global _usage_reporting_enabled
        if succeeded and _usage_reporting_enabled == None:
            _prompt_to_set_usage_reporting(callback)
        else:
            executeCallback(callback)

    run_command(["usage-reporting", "status", "--json"], on_data, on_done, True, "Checking AppBuilder CLI usage reporting")

def _prompt_to_set_usage_reporting(callback=None):
    sublime.active_window().show_input_panel("Send anonymous usage statistics to help improve your Telerik AppBuilder experience? (yes, no)", "Yes",
        lambda response=None: _set_usage_reporting(response, callback), None, lambda response=None: _set_usage_reporting(response, callback))

def _set_usage_reporting(response = None, callback = None):
    if response:
        response = response.lower()
        if response == "yes":
            run_command(["usage-reporting", "enable"], lambda data: log_info(data), lambda succeeded: executeCallback(callback), True, "Turning on usage reporting",
                "Usage reporting is now turned on", "Usage reporting could not turn on")
        elif response == "no":
            run_command(["usage-reporting", "disable"], lambda data: log_info(data), lambda succeeded: executeCallback(callback), True, "Turning off usage reporting",
                "Usage reporting is now turned off", "Usage reporting could not turn off")
        return
    _prompt_to_set_usage_reporting()

def executeCallback(callback=None):
    if callback != None:
        callback()
