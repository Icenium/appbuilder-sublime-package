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

class AppBuilderCommandsHelpers(object):
    @staticmethod
    def select_project_and_device(app_builder_command, callback):
        select_project(app_builder_command, lambda selected_project: select_device(app_builder_command, lambda selected_device: callback(selected_project, selected_device)) if selected_project != None else callback(None, None))

class DeployCommand(RegularAppBuilderCommand):
    @property
    def command_name(self):
        return "Deploy"

    def on_started(self):
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
        return "LiveSync Application"

    def on_started(self):
        AppBuilderCommandsHelpers.select_project_and_device(self, self.execute)

    def execute(self, project, device):
        if project == None or device == None:
            self.on_finished(False)
            return

        command = ["livesync", "--path", project[1]]
        command.append("--device")
        command.append(device["identifier"])
        self.run_command(command, True, "Syncing", "Sync succeeded", "Sync failed")

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
    def __init__(self):
        super(ToggleLiveSyncCommand, self).__init__()
        self.viewStatusKey = "LiveSyncStatus"
        self.projectInSync = False
        self._command_thread = None
        self.markedViews = None

    @property
    def command_name(self):
        return "Enable LiveSync on Save"

    def on_starting(self):
        AppBuilderCommandsHelpers.select_project_and_device(self, lambda project, device: self.execute(project, device))

    def execute(self, project, device):
        if project != None and device != None:
            self.projectInSync = project
            command = ["livesync", "--watch", "--path", self.projectInSync[1]]
            command.append("--device")
            command.append(device["identifier"])

            self.run_command(command)

            self.init_mark_views(self.get_window().views())
            self.subscribe_to_sublime_view_loaded()

            self.on_started()
        else:
            self.on_finished(False)

    def on_finished(self, succeeded):
        self.unsubscribe_from_sublime_view_loaded()
        if self.has_marked_views():
            self.unmark_views()

        super(ToggleLiveSyncCommand, self).on_finished(succeeded)

    def subscribe_to_sublime_view_loaded(self):
        global on_sublime_view_loaded
        on_sublime_view_loaded += self.on_view_loaded

    def unsubscribe_from_sublime_view_loaded(self):
        global on_sublime_view_loaded
        on_sublime_view_loaded += self.on_view_loaded
        on_sublime_view_loaded -= self.on_view_loaded

    def on_view_loaded(self, view):
        self.mark_view(view)

    def init_mark_views(self, views):
        self.markedViews = list()
        for view in views:
            if view.file_name():
                self.mark_view(view)

    def mark_view(self, view):
        if self.is_in_the_project(view):
            view.set_status(self.viewStatusKey, "LiveSync ON")
        else:
            view.set_status(self.viewStatusKey, "LiveSync OFF (ON for '{name}' project)".
                format(name=self.projectInSync[0]))
        self.markedViews.append(view)

    def is_in_the_project(self, view):
        return view.file_name().startswith(self.projectInSync[1])

    def has_marked_views(self):
        return self.markedViews != None and len(self.markedViews) > 0

    def unmark_views(self):
        for view in self.markedViews:
            view.erase_status(self.viewStatusKey)
        self.markedViews = None
