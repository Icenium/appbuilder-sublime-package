import os
import json
import sublime
import sublime_plugin

from .bootstrapper import has_compatible_working_appbuilder_cli
from .notifier import log_info, log_error
from .command_executor import show_quick_panel, run_command
from .sublime_events_listener import on_sublime_view_loaded
from .base_commands import AppBuilderWindowCommandBase
from .project import Project

class DevicesCommandBase(AppBuilderWindowCommandBase):
    @property
    def command_name(self):
        return ""

    def is_enabled(self):
        return has_compatible_working_appbuilder_cli()

    def run(self):
        self.do_run()

    def do_run(self):
        self.choose_project()

    def choose_project(self):
        self.projects = []

        project_dir = Project.get_project_dir(self.get_working_dir())
        if (bool(project_dir)):
            self.projects.append(project_dir)

        for index, value in enumerate(self.window.folders()):
            project_dir = Project.get_project_dir(value)
            if (bool(project_dir)):
                self.projects.append(project_dir)

        self.projects = list(set(self.projects))
        self.projects = list(map((lambda project: [Project.get_project_name(project), project]), self.projects))

        projectsCount = len(self.projects)
        if projectsCount == 1:
            self.on_project_chosen(0)
        elif projectsCount > 1:
            show_quick_panel(self, self.projects, self.on_project_chosen)
        else:
            log_info("There are no projects in your currently opened folders")

    def on_project_chosen(self, project_index):
        if project_index >= 0:
            self.choose_device(lambda device_index: self.execute(project_index, device_index))
        else:
            self.execute(project_index, -1)

    def choose_device(self, callback):
        self.on_device_chosen = callback
        command = ["list-devices", "--json"]
        self.devices = []
        run_command(command, self.on_device_data_reveived, self.on_devices_data_finished, True, "Retrieving devices")

    def on_device_data_reveived(self, data):
        try:
            device = json.loads(data)
            self.devices.append(device)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            log_error(data)

    def on_devices_data_finished(self, exit_code):
        if (exit_code == 0):
            devicesCount = len(self.devices)
            if devicesCount == 0:
                log_info("There are no connected devices")
                self.on_device_chosen(-1)
            elif devicesCount == 1:
                self.on_device_chosen(0)
            elif devicesCount > 1:
                devicesList = list(map((lambda device: [device["name"],
                        "Platform: {platform} {version}".format(platform=device["platform"], version=device["version"]),
                        "Model: {model}".format(model=device["model"]),
                        "Vendor: {vendor}".format(vendor=device["vendor"])]),
                    self.devices))
                show_quick_panel(self, devicesList, self.on_device_chosen)
        else:
            log_error("Command failed with exit code: {code}".format(code = exit_code))
            self.on_device_chosen(-1)

    def on_data(self, data):
        log_info(data)

    def on_done(self, exit_code):
        if exit_code != 0:
            log_error("Command failed with exit code: {code}".format(code = exit_code))

        log_info("Exit code: {exit_code}".format(exit_code=exit_code))

class DeployCommand(DevicesCommandBase):
    @property
    def command_name(self):
        return "Deploy"

    def execute(self, project_index, device_index):
        if project_index < 0 or device_index < 0:
            return

        command = ["deploy", "--path", self.projects[project_index][1]]
        command.append("--device")
        command.append(self.devices[device_index]["identifier"])
        run_command(command, self.on_data, self.on_done, True, "Deploying")

class SyncCommand(DevicesCommandBase):
    @property
    def command_name(self):
        return "Sync"

    def execute(self, project_index, device_index):
        if project_index < 0 or device_index < 0:
            return

        command = ["livesync", "--path", self.projects[project_index][1]]
        command.append("--device")
        command.append(self.devices[device_index]["identifier"])
        run_command(command, self.on_data, self.on_done, True, "Syncing")

class ToggleLiveSyncCommand(DevicesCommandBase):
    viewStatusKey = "LiveSyncStatus"
    isChecked = False
    isStarting = False
    commandThread = None
    projectInSync = None
    markedViews = None

    @property
    def command_name(self):
        return "Live Sync"

    def run(self):
        if ToggleLiveSyncCommand.isStarting:
            return

        ToggleLiveSyncCommand.isStarting = True

        if ToggleLiveSyncCommand.commandThread == None:
            self.do_run()
        else:
            try:
                ToggleLiveSyncCommand.commandThread.terminate()
            finally:
                ToggleLiveSyncCommand.commandThread = None
                ToggleLiveSyncCommand.isStarting = False
                ToggleLiveSyncCommand.isChecked = False

    def is_checked(self):
        return ToggleLiveSyncCommand.isChecked

    def execute(self, project_index, device_index):
        global on_sublime_view_loaded
        if project_index >= 0 and device_index >= 0:
            ToggleLiveSyncCommand.projectInSync = self.projects[project_index]
            command = ["livesync", "--watch", "--path", ToggleLiveSyncCommand.projectInSync[1]]
            command.append("--device")
            command.append(self.devices[device_index]["identifier"])

            ToggleLiveSyncCommand.commandThread = run_command(command, self.on_data, self.on_done, False)
            ToggleLiveSyncCommand.isChecked = True
            ToggleLiveSyncCommand.init_mark_views(self.window.views())
            on_sublime_view_loaded += self.on_view_loaded

        ToggleLiveSyncCommand.isStarting = False

    def on_done(self, exit_code):
        global on_sublime_view_loaded
        if exit_code != 0:
            log_error(exit_code)

        ToggleLiveSyncCommand.commandThread = None
        ToggleLiveSyncCommand.isChecked = False
        ToggleLiveSyncCommand.projectInSync = None
        on_sublime_view_loaded -= self.on_view_loaded
        ToggleLiveSyncCommand.unmark_views()

        log_info("Exit code: {exit_code}".format(exit_code=exit_code))

    def on_view_loaded(self, view):
        ToggleLiveSyncCommand.mark_view(view)

    @staticmethod
    def init_mark_views(views):
        ToggleLiveSyncCommand.markedViews = list()
        for view in views:
            ToggleLiveSyncCommand.mark_view(view)

    @staticmethod
    def mark_view(view):
        if ToggleLiveSyncCommand.is_in_the_project(view):
            view.set_status(ToggleLiveSyncCommand.viewStatusKey, "LiveSync ON")
        else:
            view.set_status(ToggleLiveSyncCommand.viewStatusKey, "LiveSync OFF (ON for '{name}' project)".
                format(name=ToggleLiveSyncCommand.projectInSync[0]))
        ToggleLiveSyncCommand.markedViews.append(view)

    @staticmethod
    def is_in_the_project(view):
        return view.file_name().startswith(ToggleLiveSyncCommand.projectInSync[1])

    @staticmethod
    def unmark_views():
        for view in ToggleLiveSyncCommand.markedViews:
            view.erase_status(ToggleLiveSyncCommand.viewStatusKey)
        ToggleLiveSyncCommand.markedViews = None

class RunInSimulatorCommand(DevicesCommandBase):
    @property
    def command_name(self):
        return "Run in Simulator"

    def run(self):
        if self.is_enabled():
            self.choose_project()

    def on_project_chosen(self, project_index):
        if project_index >= 0:
            command = ["simulate", "--path", self.projects[project_index][1]]
            run_command(command, self.on_data, self.on_done, True, "Starting simulator")