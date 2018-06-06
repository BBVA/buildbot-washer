import inspect

from buildbot_worker.commands.base import Command


class WasherCommand(Command):
    requiredArgs = ["task"]

    @staticmethod
    def run_task(sender, task):
        if not inspect.isgeneratorfunction(task):
            raise TypeError("Task must be a generator.")


def washertask():
    """`washertask` registering decorator."""
    pass
