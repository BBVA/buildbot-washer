from buildbot.plugins import steps
from buildbot.process import buildstep
from buildbot.steps.worker import CompositeStepMixin
from twisted.internet import defer

from . import remotecommand


class TriggerFromFile(steps.Trigger, CompositeStepMixin):
    renderables = steps.Trigger.renderables + ["configfile"]

    def __init__(self, configfile=None, processor=None, **kwargs):
        if configfile is None:
            configfile = ".washer.conf"

        self.configfile = configfile
        self.processor = processor
        self.config = None

        super().__init__(**kwargs)

    @defer.inlineCallbacks
    def run(self):
        self.config = yield self.getFileContentFromWorker(
            self.configfile,
            abandonOnFailure=True)
        rv = yield super().run()
        defer.returnValue(rv)

    def getSchedulersAndProperties(self):
        return list(self.processor(self))


class WasherTask(buildstep.LoggingBuildStep, CompositeStepMixin):
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
        res = yield self.runCommand(cmd)

        return res.results()
