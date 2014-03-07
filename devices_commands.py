import os
import json
import sublime
import sublime_plugin

from base_commands import AppBuilderWindowCommandBase
from command_executor import AppBuilderCommandExecutor
from project import Project
from notifier import Notifier

class DevicesCommandBase(AppBuilderWindowCommandBase):
    @property
    def command_name(self):
        return ""

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
        self.projects = map((lambda project: [Project.get_project_name(project), project]), self.projects)

        projectsCount = len(self.projects)
        if projectsCount == 1:
            self.on_project_chosen(0)
        elif projectsCount > 1:
            AppBuilderCommandExecutor.show_quick_panel(self, self.projects, self.on_project_chosen)
        else:
            Notifier.log_info("There are no projects in your currently opened folders")

    def on_project_chosen(self, project_index):
        if project_index >= 0:
            self.choose_device(lambda device_index: self.execute(project_index, device_index))

    def choose_device(self, callback):
        self.on_device_chosen = callback
        command = ["list-devices", "--json"]
        self.devices = []
        AppBuilderCommandExecutor.run_command(command, self.on_device_data_reveived, self.on_devices_data_finished, "Retrieving devices")

    def on_device_data_reveived(self, data):
        try:
            device = json.loads(data)
            self.devices.append(device)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print data

    def on_devices_data_finished(self, exit_code):
        if (exit_code == 0):
            devicesCount = len(self.devices)
            if devicesCount == 0:
                Notifier.log_info("There are no connected devices")
            elif devicesCount == 1:
                self.on_device_chosen(0)
            elif devicesCount > 1:
                devicesList = map((lambda device: [device["name"],
                        "Platform: {platform} {version}".format(platform=device["platform"], version=device["version"]),
                        "Model: {model}".format(model=device["model"]),
                        "Vendor: {vendor}".format(vendor=device["vendor"])]),
                    self.devices)
                AppBuilderCommandExecutor.show_quick_panel(self, devicesList, self.on_device_chosen)
        else:
            Notifier.log_error("Command failed with exit code: {code}".format(code = exit_code))
            self.on_device_chosen(-1)

    def on_data(self, data):
        Notifier.log_info(data)

    def on_done(self, exit_code):
        if exit_code != 0:
            Notifier.log_error("Command failed with exit code: {code}".format(code = exit_code))

        Notifier.log_info(exit_code)

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
        AppBuilderCommandExecutor.run_command(command, self.on_data, self.on_done, "Deploying")

class SyncCommand(DevicesCommandBase):
    @property
    def command_name(self):
        return "Sync"

    def execute(self, project_index, device_index):
        if project_index < 0 or device_index < 0:
            return

        command = ["live-sync", "--path", self.projects[project_index][1]]
        command.append("--device")
        command.append(self.devices[device_index]["identifier"])
        AppBuilderCommandExecutor.run_command(command, self.on_data, self.on_done, "Syncing")

class ToggleLiveSyncCommand(DevicesCommandBase):
    @property
    def command_name(self):
        return "Live Sync"

    isChecked = False
    isStarting = False
    commandThread = None

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
        if project_index >= 0 and device_index >= 0:
            command = ["live-sync", "--watch", "--path", self.projects[project_index][1]]
            command.append("--device")
            command.append(self.devices[device_index]["identifier"])

            ToggleLiveSyncCommand.commandThread = AppBuilderCommandExecutor.run_command(command, self.on_data, self.on_done, "Watching")
            ToggleLiveSyncCommand.isChecked = True

        ToggleLiveSyncCommand.isStarting = False

    def on_done(self, exit_code):
        if exit_code != 0:
            Notifier.log_error(exit_code)

        ToggleLiveSyncCommand.commandThread = None
        ToggleLiveSyncCommand.isChecked = False
        Notifier.log_info(exit_code)

class RunInSimulatorCommand(DevicesCommandBase):
    @property
    def command_name(self):
        return "Run in Simulator"

    def run(self):
        if os.name == "nt":
            self.choose_project()

    def on_project_chosen(self, project_index):
        if project_index >= 0:
            command = ["simulate", "--path", self.projects[project_index][1]]
            AppBuilderCommandExecutor.run_command(command, self.on_data, self.on_done, "Starting simulator")
