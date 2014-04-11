import os
import json
import sublime
import sublime_plugin
import abc

from .bootstrapper import has_compatible_working_appbuilder_cli
from .notifier import log_info, log_error
from .command_executor import show_quick_panel, run_command
from .sublime_events_listener import on_sublime_view_loaded
from .base_commands import AppBuilderWindowCommandBase
from .project import Project
from .projects_space import select_project
from .devices_space import select_device

class DeployCommand(AppBuilderWindowCommandBase):
    @property
    def command_name(self):
        return "Deploy"

    def run(self):
        AppBuilderCommandsHelpers.select_project_and_device(self, self.execute)

    def execute(self, project, device):
        if project == None or device == None:
            return

        command = ["deploy", "--path", project[1]]
        command.append("--device")
        command.append(self.devices[device_index]["identifier"])
        run_command(command, lambda data: log_info(data), self.on_done, True, "Deploying", "Deployment succeeded", "Deployment failed")

    def on_done(succeeded):
        pass

class SyncCommand(AppBuilderWindowCommandBase):
    @property
    def command_name(self):
        return "Sync"

    def run(self):
        AppBuilderCommandsHelpers.select_project_and_device(self, self.execute)

    def execute(self, project_index, device_index):
        if project_index < 0 or device_index < 0:
            return

        command = ["livesync", "--path", self.projects[project_index][1]]
        command.append("--device")
        command.append(self.devices[device_index]["identifier"])
        run_command(command, self.on_data, self.on_done, True, "Syncing", "Sync succeeded", "Sync failed")

    def on_done(self, succeeded):
        pass

class ToggleLiveSyncCommand(AppBuilderWindowCommandBase):
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
            self.run_implementation()
        else:
            try:
                ToggleLiveSyncCommand.commandThread.terminate()
            finally:
                ToggleLiveSyncCommand.commandThread = None
                ToggleLiveSyncCommand.isStarting = False
                ToggleLiveSyncCommand.isChecked = False

    def is_checked(self):
        return ToggleLiveSyncCommand.isChecked

    def execute(self, project, device):
        global on_sublime_view_loaded
        if project != None and device != None:
            ToggleLiveSyncCommand.projectInSync = project
            command = ["livesync", "--watch", "--path", ToggleLiveSyncCommand.projectInSync[1]]
            command.append("--device")
            command.append(device["identifier"])

            ToggleLiveSyncCommand.commandThread = run_command(command, self.on_data, self.on_done, False)
            ToggleLiveSyncCommand.isChecked = True
            ToggleLiveSyncCommand.init_mark_views(self.window.views())
            on_sublime_view_loaded += self.on_view_loaded

        ToggleLiveSyncCommand.isStarting = False

    def on_done(self, succeeded):
        super(ToggleLiveSyncCommand, self).on_done(succeeded)

        global on_sublime_view_loaded
        ToggleLiveSyncCommand.commandThread = None
        ToggleLiveSyncCommand.isChecked = False
        ToggleLiveSyncCommand.projectInSync = None
        on_sublime_view_loaded -= self.on_view_loaded
        ToggleLiveSyncCommand.unmark_views()

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

class RunInSimulatorCommand(AppBuilderWindowCommandBase):
    @property
    def command_name(self):
        return "Run in Simulator"

    def is_enabled(self):
        return super(RunInSimulatorCommand, self).is_enabled() and os.name == "nt"

    def is_visible(self):
        return os.name == "nt"

    def run(self):
        select_project(self, self.on_project_chosen)

    def on_project_chosen(self, project):
        if project != None:
            command = ["simulate", "--path", project[1]]
            run_command(command, self.on_data, self.on_done, True, "Starting simulator", "Simulator started", "Simulator could not start")

    def on_data(self, data):
        log_info(data)

    def on_done(self, succeeded):
        pass

class AppBuilderCommandsHelpers(object):
    @staticmethod
    def select_project_and_device(app_builder_command, callback):
        select_project(app_builder_command, lambda selected_project: select_device(app_builder_command, lambda selected_device: callback(selected_project, selected_device)) if selected_project != None else callback(None, None))
