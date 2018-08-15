from buildbot.plugins import steps
from buildbot.steps.worker import CompositeStepMixin
from twisted.internet import defer


class TriggerFromFile(steps.Trigger, CompositeStepMixin):
    """
    Allows dynamic triggering of schedulers depending on data present on a
    repository file.

    Read the file `configfile` from the user repository and invoke `processor`.

    `processor` should be a generator yielding dictionaries with 3 keys:

    * `sched_name`: The name of the scheduler to trigger.
    * `props_to_set`: A dictionaries mapping which `Properties` to set.
    * `unimportant`: A boolean value. If set to `True`, a fail on the triggered
                     scheduled will not cause this step to fail.

    """
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
