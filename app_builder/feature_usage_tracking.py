import sublime
import json

from .command_executor import run_command
from .notifier import log_info

_track_feature_usage_enabled = None

def ensure_feature_usage_tracking_is_set(callback=None):
    if _track_feature_usage_enabled != None:
        return

    def on_data(data):
        global _track_feature_usage_enabled
        if _track_feature_usage_enabled == None:
            try:
                parsed_data = json.loads(data)
                _track_feature_usage_enabled = parsed_data["enabled"]
            except ValueError: # includes simplejson.decoder.JSONDecodeError
                pass

    def on_done(succeeded):
        global _track_feature_usage_enabled
        if succeeded and _track_feature_usage_enabled == None:
            _prompt_to_set_feature_usage_tracking(callback)
        else:
            executeCallback(callback)

    run_command(["feature-usage-tracking", "status", "--json"], on_data, on_done, True, "Checking AppBuilder CLI feature usage tracking")

def _prompt_to_set_feature_usage_tracking(callback=None):
    sublime.active_window().show_input_panel("Send anonymous usage statistics to help improve your Telerik AppBuilder experience? (yes, no)", "Yes",
        lambda response: _set_feature_usage_tracking(response, callback), None, lambda response: _set_feature_usage_tracking(response, callback))

def _set_feature_usage_tracking(response = None, callback = None):
    if response:
        response = response.lower()
        if response == "yes":
            run_command(["feature-usage-tracking", "enable"], lambda data: log_info(data), lambda succeeded: executeCallback(callback), True, "Turning on feature usage tracking",
                "Feature usage tracking is now turned on", "Feature usage tracking could not turn on")
        elif response == "no":
            run_command(["feature-usage-tracking", "disable"], lambda data: log_info(data), lambda succeeded: executeCallback(callback), True, "Turning off feature usage tracking",
                "Feature usage tracking is now turned off", "Feature usage tracking could not turn off")
        return
    _prompt_to_set_feature_usage_tracking()

def executeCallback(callback=None):
    if callback != None:
        callback()
