import sublime
import os
import json

from .notifier import log_info, log_fail
from .semver import *
from .helpers import *

_has_compatible_working_appbuilder_cli = None
_config = None

def initialize(installed_appbuilder_cli_version):
    _verify_appbuilder_cli_version(installed_appbuilder_cli_version)

def _load_config():
    global _config
    settings = sublime.load_settings("telerik_appbuilder.sublime-settings")
    _config = {
        "osx_node_path": settings.get("node_osx_path") or "/usr/local/bin/node",
        "osx_appbuilder_path": settings.get("appbuilder_osx_path") or "/usr/local/bin/appbuilder",
        "linux_node_path": settings.get("linux_node_path") or "",
        "linux_appbuilder_path": settings.get("linux_appbuilder_path") or "",
        "win_node_name": "node",
        "win_appbuilder_name": "appbuilder",
        "min_required_appbuilder_cli_version": "2.14.0", #inclusive
        "max_allowed_appbuilder_cli_version": "2.15.0"  #exclusive
    }

def _verify_appbuilder_cli_version(installed_appbuilder_cli_version):
    global _has_compatible_working_appbuilder_cli
    min_required_appbuilder_cli_version = get_config("min_required_appbuilder_cli_version")
    max_allowed_appbuilder_cli_version = get_config("max_allowed_appbuilder_cli_version")
    cli_version = get_correct_semversion(installed_appbuilder_cli_version)
    validMinVersion = match(cli_version, ">="+min_required_appbuilder_cli_version)
    validMaxVersion = match(cli_version, "<"+max_allowed_appbuilder_cli_version)
    if validMinVersion and validMaxVersion:
        _has_compatible_working_appbuilder_cli = True
        log_info("Telerik AppBuilder has been initialized successfully")
    else:
        _has_compatible_working_appbuilder_cli = False
        if not validMinVersion:
            log_fail("You have updated your Telerik AppBuilder package to {required_min_version}.\n".
                format(required_min_version=min_required_appbuilder_cli_version) +
                "To be able to load it, you need to update your Telerik AppBuilder CLI to {installed_version}.x.".
                format(installed_version=".".join(get_major_minor_version_from_string(min_required_appbuilder_cli_version))))
        if not validMaxVersion:
            log_fail("You have updated your Telerik AppBuilder CLI to {cli_version}.\n".
                format(cli_version=installed_appbuilder_cli_version) +
                "To be able to load the Telerik AppBuilder package, you need to update the package to at least {required_min_version}.0.".
                format(required_min_version=".".join(get_major_minor_version_from_string(installed_appbuilder_cli_version))))

def get_config(name):
    global _config
    if _config == None:
        _load_config()

    return _config[name]

def has_compatible_working_appbuilder_cli():
    global _has_compatible_working_appbuilder_cli
    return bool(_has_compatible_working_appbuilder_cli)