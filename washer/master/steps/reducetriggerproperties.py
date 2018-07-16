from buildbot import config
from buildbot.plugins import steps
from buildbot.process.buildstep import BuildStep
from buildbot.process.buildstep import SUCCESS
from buildbot.steps.trigger import Trigger
from twisted.internet import defer


class ReduceTriggerProperties(BuildStep):
    requiredArgs = ["reducefn"]
    name = "reducetrigger"
    haltOnFailure = True
    flunkOnFailure = True

    def __init__(self, reducefn=None, **kwargs):
        if reducefn is None:
            config.error("reducefn must be set")  # This raises an exception
        else:
            self.reducefn = reducefn
        super().__init__(**kwargs)

    def get_last_step_build_requests(self):
        try:
            last_step = self.build.executedSteps[-2]  # because [-1] is self
        except AttributeError as exc:
            raise RuntimeError(
                "ReduceTriggerProperties depends on build's"
                " `executedSteps`.") from exc
        except IndexError as exc:
            raise RuntimeError(
                "This can't be the first step in the factory") from exc
        else:
            if not isinstance(last_step, Trigger):
                raise TypeError("Previous step must descend from Trigger.")
            if not getattr(last_step, "waitForFinish", True):
                raise ValueError(
                    "Previous step `waitForFinish` must be `True`.")
            return last_step.brids

    @defer.inlineCallbacks
    def get_buildrequest_builds(self, buildrequestid):
        builds = yield self.master.data.get(
            ("buildrequests", buildrequestid, "builds"))
        return [build["buildid"] for build in builds]

    def get_build_properties(self, buildid):
        return self.master.data.get(
            ("builds", buildid, "properties"))

    @staticmethod
    def clean_build_properties(properties):
        """
        Build properties contain descriptions; this method remove them.
          {k: (v, dsc)} -> {k: v}

        """
        return {k: v[0] for k, v in properties.items()}

    @defer.inlineCallbacks
    def get_previous_trigger_properties(self):
        trigger_properties = list()

        for build_request in self.get_last_step_build_requests():
            builds = yield self.get_buildrequest_builds(build_request)

            for build in builds:
                properties = yield self.get_build_properties(build)

                clean_properties = self.clean_build_properties(properties)
                trigger_properties.append(clean_properties)

        return trigger_properties

    @defer.inlineCallbacks
    def run(self):
        properties = yield self.get_previous_trigger_properties()

        # Give a chance to `reducefn` to execute but only add the properties if
        # there is any.
        reduced = self.reducefn(*properties)
        if reduced:
            for key, value in reduced.items():
                self.setProperty(key, value, self.name, runtime=True)

        defer.returnValue(SUCCESS)
