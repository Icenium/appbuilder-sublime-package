import threading
import subprocess
import os
import sublime
import functools

from .notifier import log_info, log_error, log_warning

def main_thread(callback, *args, **kwargs):
    sublime.set_timeout(functools.partial(callback, *args, **kwargs), 0)

class CommandThread(threading.Thread):
    def __init__(self, command, on_data, on_done, **kwargs):
        threading.Thread.__init__(self)
        self.command = command
        self.on_data = on_data
        self.on_done = on_done
        if "stdin" in kwargs:
            self.stdin = kwargs["stdin"]
        else:
            self.stdin = subprocess.PIPE
        if "stdout" in kwargs:
            self.stdout = kwargs["stdout"]
        else:
            self.stdout = subprocess.PIPE
        self.kwargs = kwargs

    def terminate(self):
        if self.proc != None:
            self.proc.stdin.close()

    def run(self):
        try:
            startupinfo = None
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW

            self.proc = subprocess.Popen(self.command,
                stdout=self.stdout, stderr=subprocess.STDOUT, stdin=self.stdin,
                shell=False, universal_newlines=True, startupinfo=startupinfo)

            if self.on_data:
                for line in iter(self.proc.stdout.readline, ""):
                    main_thread(self.on_data, line)

            self.proc.wait();

            if self.proc.returncode != 0:
                main_thread(log_error, CommandThread._get_command_failed_message(e.returncode))

            main_thread(self.on_done, self.proc.returncode == 0)

        except subprocess.CalledProcessError as e:
            main_thread(log_warning, CommandThread._get_command_failed_message(e.returncode))
            main_thread(self.on_done, False)
        except OSError as e:
            if e.errno == 2:
                main_thread(log_warning, "AppBuilder could not be found in PATH\nPATH is: %s" % os.environ["PATH"])
                main_thread(self.on_done, False)
            else:
                raise e

    def success(self):
        if self.is_alive():
            return False;
        else:
            return self.proc and self.proc.returncode == 0

    @staticmethod
    def _get_command_failed_message(exit_code):
        return "Command failed with exit code: {code}".format(code = exit_code)