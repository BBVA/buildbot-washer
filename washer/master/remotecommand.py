from twisted.internet import defer
from buildbot.process import remotecommand
from buildbot.process import results


class WasherTaskCommand(remotecommand.RemoteCommand):
    """
    Master side of a washer task.

    """
    def __init__(self, task_name=None, task_args=None):

        if task_name is None:
            task_name = "main"

        if task_args is None:
            task_args = {}

        remotecommand.RemoteCommand.__init__(
            self,
            "washertask",
            {"task_name": task_name,
             "task_args": task_args},
            decodeRC={results.SUCCESS: results.SUCCESS,
                      results.FAILURE: results.FAILURE,
                      results.EXCEPTION: results.EXCEPTION,
                      results.WARNINGS: results.WARNINGS})

    @defer.inlineCallbacks
    def remoteUpdate(self, update):
        """
        Translate messages received from the worker to actions performed on the
        master.

        """
        for name, value in update.get("progress", {}).items():
            self.step.setProgress(name, value)

        if "summary" in update:
            self.step.description = update["summary"]
            self.step.updateSummary()

        if "createlog" in update:
            logname = update["createlog"]
            if logname not in self.step.logfiles:
                logfile = self.step.addLogForRemoteCommands(logname)
                self.step.logfiles[logname] = logfile
                self.useLog(logfile, False, logname)

        if "property" in update:
            name, value = update["property"]
            self.step.setProperty(name, value, self.step.name, runtime=True)

        yield super().remoteUpdate(update)
