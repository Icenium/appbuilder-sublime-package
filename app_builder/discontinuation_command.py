import sublime
import sublime_plugin
import os.path
from .notifier import log_fail, log_info

class DiscontinuationCommand(sublime_plugin.ApplicationCommand):
    @property
    def command_name(self):
        return "Discontinuation"

    def run(self):
        msg = "The Telerik Platform product is retired as of May 10, 2018. For more information about the discontinuation and how you can recover your apps or data, please see the full announcement here: https://www.telerik.com/platform-next-level"
        additionalMsg = "Telerik recommends NativeScript Sidekick (https://www.nativescript.org/nativescript-sidekick) for developing modern, cross-platform mobile apps with web technologies like JavaScript, Angular, or Vue.js, and Kinvey (https://www.kinvey.com/) for hosting critical business back-end in the cloud."
        log_fail(msg)
        log_info(additionalMsg)

    def is_enabled(self):
        return True