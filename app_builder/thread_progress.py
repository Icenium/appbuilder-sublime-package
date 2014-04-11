import sublime

addend = 1
size = 8
iterations_before_release = 20

_commandsInProgress = []

def run_progress_indicator(thread, message, success_message, fail_message):
    global _commandsInProgress
    _commandsInProgress.append(CommandInProgressModel(thread, message, success_message, fail_message))

    if len(_commandsInProgress) == 1:
        _run(0)

def _add_command(commandInProgressModel):
    global _commandsInProgress
    _commandsInProgress.append(commandInProgressModel)

def _run(r):
    global _commandsInProgress
    if len(_commandsInProgress) >= 1:
        in_progress_part = _get_in_progress_part()
        finished_part = _get_finished_part()
        busy_animation_part = _get_busy_animation_part(r)

        status_message = ""
        if in_progress_part:
            status_message = "%s %s %s" % \
                (in_progress_part, busy_animation_part, finished_part)
        else:
            status_message = "%s" % \
                (finished_part)

        sublime.status_message(status_message)

        _update_commands_models()
        sublime.set_timeout(lambda: _run(r + addend), 100)
    else:
        sublime.status_message("")

def _update_commands_models():
    global _commandsInProgress
    _commandsInProgress = [commandModel for commandModel in _commandsInProgress if not commandModel.can_release()]

def _get_in_progress_part():
    global _commandsInProgress
    in_progress_commands_messages = [commandModel.message for commandModel in _commandsInProgress if commandModel.is_running()]
    return " | ".join(in_progress_commands_messages)

def _get_finished_part():
    global _commandsInProgress
    finished_commands_messages = [commandModel.get_result_message() for commandModel in _commandsInProgress if not commandModel.is_running()
        and commandModel.get_result_message() != ""]
    return " | ".join(finished_commands_messages);

def _get_busy_animation_part(r):
    before = r % size
    after = (size - 1) - before

    if not after:
        addend = -1
    if not before:
        addend = 1

    return "[%s = %s]" % \
        ("-" * before, "-" * after)

class CommandInProgressModel:
    def __init__(self, thread, message, success_message, fail_message):
        global iterations_before_release
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.fail_message = fail_message

        self.iterations_before_release = iterations_before_release

    def is_running(self):
        return self.thread.is_alive()

    def get_result_message(self):
        if not self.thread.is_alive():
            self.iterations_before_release -= 1

            if hasattr(self.thread, "result") and not self.thread.result:
                return ""

            if self.thread.success():
                return self.success_message;
            else:
                return self.fail_message;
        else:
            return "";

    def can_release(self):
        return self.iterations_before_release == 0
