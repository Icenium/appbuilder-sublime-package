import sublime
import json

sublime_version = 2

if sublime.version() == '' or int(sublime.version()) > 3000:
    sublime_version = 3

try:
    # Python 3
    from .app_builder import *
    from .app_builder import command_executor
    from .app_builder import bootstrapper
    from .app_builder.notifier import log_fail
    from .app_builder.helpers import parse_version_string

except (ValueError):
    # Python 2
    from app_builder import *
    from app_builder import command_executor
    from app_builder import bootstrapper
    from app_builder.notifier import log_fail
    from app_builder.helpers import parse_version_string

def plugin_loaded():
    installed_appbuilder_cli_version = None
    def on_data(data):
        global installed_appbuilder_cli_version
        if data:
            installed_appbuilder_cli_version = parse_version_string(data)

    def on_done(succeeded):
        global installed_appbuilder_cli_version
        if succeeded:
            bootstrapper.initialize(installed_appbuilder_cli_version)
        else:
            installed_appbuilder_cli_version = None
            log_fail("Cannot load the Telerik AppBuilder package because the Telerik AppBuilder command-line interface is not installed properly on your system.\n" +
                "For a complete list of the system requirements for running the Telerik AppBuilder package, go to:\n" +
                "https://github.com/Icenium/appbuilder-sublime-package#installation")

    command_executor.run_command(["--version"], on_data, on_done, True, "Checking AppBuilder CLI version")

if sublime_version == 2:
    plugin_loaded()
