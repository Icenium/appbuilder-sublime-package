import sublime
import os
import json

from .notifier import log_info, log_fail
from .helpers import parse_version_string

_has_compatible_working_appbuilder_cli = None
_config = None

def initialize(installed_appbuilder_cli_version):
    _load_config()
    _verify_appbuilder_cli_version(installed_appbuilder_cli_version)

def _load_config():
    global _config
    _settings = sublime.load_settings("AppBuilder.sublime-settings")
    _config = {
        "osx_node_path": settings.get("node_osx_path") or "/usr/local/bin/node",
        "osx_appbuilder_path": settings.get("osx_appbuilder_path") or "/usr/local/bin/appbuilder",
        "win_node_name": "node",
        "win_appbuilder_name": "appbuilder",
        "required_appbuilder_cli_version": "2.0.1"
    }

def _verify_appbuilder_cli_version(installed_appbuilder_cli_version):
    global _has_compatible_working_appbuilder_cli
    required_appbuilder_cli_version = parse_version_string(get_config("required_appbuilder_cli_version"))
    if installed_appbuilder_cli_version == required_appbuilder_cli_version:
        _has_compatible_working_appbuilder_cli = True
        log_info("Telerik AppBuilder has been initialized successfuly")
    else:
        _has_compatible_working_appbuilder_cli = False
        log_fail("Cannot load the Telerik AppBuilder package because the required version of Telerik AppBuilder command-line interface is {required_version}.\n".
            format(required_version=".".join(required_appbuilder_cli_version)) +
            "The Telerik AppBuilder command-line interface version that has been found is {installed_version}".
            format(installed_version=".".join(installed_appbuilder_cli_version)))

def get_config(name):
    global _config
    return _config[name]

def has_compatible_working_appbuilder_cli():
    global _has_compatible_working_appbuilder_cli
    return bool(_has_compatible_working_appbuilder_cli)