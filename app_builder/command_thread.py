import threading
import subprocess
import os
import sublime
import functools
import notifier

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
            main_thread(self.on_done, self.proc.returncode)

        except subprocess.CalledProcessError, e:
            main_thread(self.on_done, e.returncode)
        except OSError, e:
            if e.errno == 2:
                main_thread(notifier.log_error, "AppBuilder could not be found in PATH\nPATH is: %s" % os.environ['PATH'])
            else:
                raise e

    def success(self):
        if self.is_alive():
            return False;
        else:
            return self.proc.returncode == 0