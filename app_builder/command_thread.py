import threading
import subprocess
import os
import sublime
import functools
import psutil

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
            self.stdin = None
        if "stdout" in kwargs:
            self.stdout = kwargs["stdout"]
        else:
            self.stdout = subprocess.PIPE
        self.kwargs = kwargs

    def terminate(self):
        if self.proc != None:
            self._terminate_proc_tree(self.proc.pid)

    def _terminate_proc_tree(self, pid, including_parent=True):
        parent = psutil.Process(pid)
        for child in parent.get_children(recursive=True):
            child.terminate()
        if including_parent:
            parent.terminate()

    def run(self):
        try:
            # Per http://bugs.python.org/issue8557 shell=True is required to
            # get $PATH on Windows. Yay portable code.
            shell = os.name == 'nt'

            self.proc = subprocess.Popen(self.command,
                stdout=self.stdout, stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                shell=shell, universal_newlines=True)

            if self.on_data:
                for line in self.proc.stdout:
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