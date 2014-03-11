import sublime

class Notifier(object):
    @staticmethod
    def log_info(message):
        Notifier._show_panel()
        print message

    @staticmethod
    def log_warning(message):
        Notifier.log_info(message)

    @staticmethod
    def log_error(message):
        Notifier.log_info(message)

    @staticmethod
    def _show_panel():
        window = sublime.active_window()
        window.run_command("show_panel", {"panel": "console"})
