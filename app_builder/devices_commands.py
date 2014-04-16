import os
import sublime
import sublime_plugin
import abc

from .bootstrapper import has_compatible_working_appbuilder_cli
from .notifier import log_info, log_error
from .sublime_events_listener import on_sublime_view_loaded
from .base_commands import RegularAppBuilderCommand, ToggleAppBuilderCommand
from .project import Project
from .projects_space import select_project
from .devices_space import select_device

class DeployCommand(RegularAppBuilderCommand):
    @property
    def command_name(self):
        return "Deploy"

    def run(self):
        AppBuilderCommandsHelpers.select_project_and_device(self, self.execute)

    def execute(self, project, device):
        if project == None or device == None:
            self.on_finished(False)
            return

        command = ["deploy", "--path", project[1]]
        command.append("--device")
        command.append(device["identifier"])
        self.run_command(command, True, "Deploying", "Deployment succeeded", "Deployment failed")

class SyncCommand(RegularAppBuilderCommand):
    @property
    def command_name(self):
        return "Sync"

    def on_started(self):
        AppBuilderCommandsHelpers.select_project_and_device(self, self.execute)

    def execute(self, project, device):
        if project == None or device == None:
            self.on_finished(False)
            return

        command = ["livesync", "--path", project[1]]
        command.append("--device")
        command.append(device["identifier"])
        run_command(command, True, "Syncing", "Sync succeeded", "Sync failed")

class RunInSimulatorCommand(RegularAppBuilderCommand):
    @property
    def command_name(self):
        return "Run in Simulator"

    def is_enabled(self):
        return super(RunInSimulatorCommand, self).is_enabled() and os.name == "nt"

    def is_visible(self):
        return os.name == "nt"

    def on_started(self):
        select_project(self, self.on_project_selected)

    def on_project_selected(self, project):
        if project == None:
            self.on_finished(False)
        else:
            command = ["simulate", "--path", project[1]]
            self.run_command(command, True, "Starting simulator", "Simulator started", "Simulator could not start")

class ToggleLiveSyncCommand(ToggleAppBuilderCommand):
    viewStatusKey = "LiveSyncStatus"
    projectInSync = None

    @property
    def command_name(self):
        return "Live Sync"

    def on_starting(self):
        AppBuilderCommandsHelpers.select_project_and_device(self, lambda project, device: self.execute(project, device))

    def execute(self, project, device):
        global on_sublime_view_loaded
        if project != None or device != None:
            ToggleLiveSyncCommand.projectInSync = project
            command = ["livesync", "--watch", "--path", ToggleLiveSyncCommand.projectInSync[1]]
            command.append("--device")
            command.append(device["identifier"])

            self.run_command(command)
            ToggleLiveSyncCommand.init_mark_views(self.window.views())
            on_sublime_view_loaded += self.on_view_loaded

        self.on_started()

    def on_finished(self, succeeded):
        global on_sublime_view_loaded
        on_sublime_view_loaded -= self.on_view_loaded
        ToggleLiveSyncCommand.unmark_views()
        super(ToggleAppBuilderCommand, self).on_finished(succeded)

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

class AppBuilderCommandsHelpers(object):
    @staticmethod
    def select_project_and_device(app_builder_command, callback):
        select_project(app_builder_command, lambda selected_project: select_device(app_builder_command, lambda selected_device: callback(selected_project, selected_device)) if selected_project != None else callback(None, None))
