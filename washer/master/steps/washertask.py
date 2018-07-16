from buildbot.plugins import steps
from buildbot.process import buildstep
from buildbot.steps.worker import CompositeStepMixin
from twisted.internet import defer

from washer.master import remotecommand


class WasherTask(buildstep.LoggingBuildStep, CompositeStepMixin):
    """
    This step run the washer task `task_name` with the parameters `task_args`
    on a worker.

    """
    name = "WasherTask"
    haltOnFailure = True
    flunkOnFailure = True
    useProgress = True
    renderables = (buildstep.LoggingBuildStep.renderables
                   + ["task_name", "task_args"])

    def __init__(self, task_name=None, task_args=None, **kwargs):
        self.task_name = task_name
        self.task_args = task_args
        super().__init__(**kwargs)

    @defer.inlineCallbacks
    def run(self):
        self.checkWorkerHasCommand("washertask")

        cmd = remotecommand.WasherTaskCommand(
            task_name=self.task_name,
            task_args=self.task_args)
        self.logfiles["stdio"] = yield self.addLogForRemoteCommands("stdio")
        cmd.useLog(self.logfiles["stdio"], False, "stdio")
        res = yield self.runCommand(cmd)
        defer.returnValue(res.results())
