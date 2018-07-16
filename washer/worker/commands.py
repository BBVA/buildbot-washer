import inspect
import traceback

from buildbot.process import results
from buildbot_worker.commands import registry
from buildbot_worker.commands.base import Command
from twisted.internet import reactor, defer, threads

from . import actions


__all__ = ["washertask"]


class WasherTask(Command):
    """
    Run the specified task in an independent thread, sending back to master the
    *actions* yielded by the task.

    """
    requiredArgs = ["task_name", "task_args"]

    #: User registered tasks.
    _tasks = dict()

    #: Name to be registered with into the `commandRegistry`.
    _name = "washertask"

    @staticmethod
    def runtask(sender, task, args=None):
        """
        Run a `task` and send yielded actions through `sender`.

        .. note:: This method is run in a different thread.

        """
        if not inspect.isgeneratorfunction(task):
            raise AttributeError("Task must be a generator.")

        events = task(**(args if args is not None else {}))
        has_warnings = False

        while True:
            try:
                # Advance the task execution to the next `yield` or `return`.
                event = next(events)
            except StopIteration as exc:
                # Task ended. Translate the return value to something known to
                # the master.
                if exc.value is True:
                    if has_warnings:
                        return results.WARNINGS
                    else:
                        return results.SUCCESS
                elif exc.value is False:
                    return results.FAILURE
                else:
                    raise TypeError(("Invalid return value. "
                                     "Must be either `True` or `False`."))
            except Exception as exc:
                # An internal task exception is wrapped on a RuntimeError.
                raise RuntimeError(
                    "Task exception.\n%s" % traceback.format_exc())
            else:
                # The yielded task action is check.
                if not isinstance(event, actions.MasterAction):
                    raise TypeError("Yielded values must be actions.")

                # Any yielded `Warn` will mark this task forever.
                if isinstance(event, actions.Warn):
                    has_warnings = True

                # The action message is sent to the master.
                threads.blockingCallFromThread(reactor, sender, event.message)

    def setup(self, args):
        """Assign command arguments to instance attributes."""
        self.task_name = args["task_name"]
        self.task_args = args["task_args"]
        try:
            self.task = self._tasks[self.task_name]
        except KeyError:
            raise RuntimeError("Unknown washertask %r" % self.task_name)

    @defer.inlineCallbacks
    def start(self):
        """Run `self.task` with `self.task_args` in a thread."""
        task = threads.deferToThread(
            self.runtask,
            self.sendStatus,
            self.task,
            self.task_args)

        def cb(status):
            self.sendStatus({"rc": status})

        def eb(f):
            self.sendStatus({"stderr": f.getTraceback()})
            self.sendStatus({"rc": results.EXCEPTION})

        task.addCallbacks(cb, eb)

        yield task

        # self.runtask(lambda *_: None, self.task, self.task_args)
        # yield None


def washertask(fn):
    """`washertask` registering decorator."""
    WasherTask._tasks[fn.__name__] = fn
    return fn


def register():
    """Register available washer commands into worker `commandRegistry`."""
    registry.commandRegistry[WasherTask._name] = WasherTask
