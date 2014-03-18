import os
import sys
import threading
import psutil
import subprocess
from threading import Timer

class CommandWrapper:
    def __init__(self):
        self.proc = None
        self.sublime_text_process = None

    def run(self, command_array):
        # Per http://bugs.python.org/issue8557 shell=True is required to
        # get $PATH on Windows. Yay portable code.
        shell = os.name == "nt"

        self.proc = psutil.Popen(command_array, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, shell=shell, universal_newlines=True)
        self.sublime_text_process = self.proc.parent.parent

        self._poll_processes_every(0.25)

    def _poll_processes_every(self, interval):
        if self.proc.is_running():
            if not self.sublime_text_process.is_running():
                self.terminate()
            else:
                Timer(interval, self._poll_processes_every, [interval]).start()
        else:
            sys.exit()

    def terminate(self):
        if self.proc != None:
            self._terminate_proc_tree()
        sys.exit()

    def _terminate_proc_tree(self, including_parent=True):
        parent = self.proc
        for child in parent.get_children(recursive=True):
            child.terminate()
        if including_parent:
            parent.terminate()

command = CommandWrapper()
command.run(sys.argv[1:])

