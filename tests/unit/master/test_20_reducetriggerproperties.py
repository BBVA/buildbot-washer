from collections import ChainMap
from unittest.mock import Mock

from buildbot import config
from buildbot.process import results
from buildbot.steps.trigger import Trigger
from twisted.internet import defer
import pytest
import pytest_twisted as pt

from washer.master import steps


def test_defaults():
    step = steps.ReduceTriggerProperties(reducefn=lambda:None)
    assert step.name == 'reducetrigger'
    assert step.haltOnFailure is True
    assert step.flunkOnFailure is True


def test_reducefn():
    def myreducefn():
        pass

    step = steps.ReduceTriggerProperties(reducefn=myreducefn)
    assert step.reducefn == myreducefn


def test_reducefn_not_given():
    with pytest.raises(config.ConfigErrors):
        step = steps.ReduceTriggerProperties()


def test_get_last_step_build_requests_no_executedSteps():
    step = steps.ReduceTriggerProperties(reducefn=lambda:None)

    step.build = None

    with pytest.raises(RuntimeError):
        step.get_last_step_build_requests()


def test_get_last_step_build_requests_no_enough_executed_steps():
    step = steps.ReduceTriggerProperties(reducefn=lambda:None)

    class FakeBuild:
        executedSteps = []

    step.build = FakeBuild()

    with pytest.raises(RuntimeError):
        step.get_last_step_build_requests()


def test_get_last_step_build_requests_step_is_not_trigger():
    step = steps.ReduceTriggerProperties(reducefn=lambda:None)

    class FakeBuild:
        executedSteps = [object(), step]

    step.build = FakeBuild()

    with pytest.raises(TypeError):
        step.get_last_step_build_requests()


def test_get_last_step_build_requests_waitForFinish_must_be_True():
    step = steps.ReduceTriggerProperties(reducefn=lambda:None)

    class FakeBuild:
        executedSteps = [Trigger(waitForFinish=False,
                                 schedulerNames=["NA"]),
                         step]

    step.build = FakeBuild()

    with pytest.raises(ValueError):
        step.get_last_step_build_requests()


def test_get_last_step_build_requests_return_brids():
    step = steps.ReduceTriggerProperties(reducefn=lambda:None)
    trigger = Trigger(waitForFinish=True, schedulerNames=["NA"])
    trigger.brids = object()

    class FakeBuild:
        executedSteps = [trigger, step]

    step.build = FakeBuild()

    assert step.get_last_step_build_requests() is trigger.brids


@pt.inlineCallbacks
def test_get_buildrequest_builds():
    step = steps.ReduceTriggerProperties(reducefn=lambda:None)
    step.master = Mock()

    expected = [object(), object(), object()]

    step.master.data.get.return_value = [{"buildid": o} for o in expected]
    buildrequestid = object()

    returned = yield step.get_buildrequest_builds(buildrequestid)

    step.master.data.get.assert_called_once_with(
        ("buildrequests", buildrequestid, "builds"))

    assert returned == expected


def test_get_build_properties():
    step = steps.ReduceTriggerProperties(reducefn=lambda:None)
    step.master = Mock()
    step.master.data.get.return_value = object()
    buildid = object()

    returned = step.get_build_properties(buildid)

    step.master.data.get.assert_called_once_with(
        ("builds", buildid, "properties"))

    assert returned is step.master.data.get.return_value


def test_clean_build_properties():
    o1, o2, o3 = object(), object(), object()

    build_properties = {"prop1": (o1, "dsc1"),
                        "prop2": (o2, "dsc2"),
                        "prop3": (o3, "dsc3")}

    expected = {k: v[0] for k, v in build_properties.items()}

    current = steps.ReduceTriggerProperties.clean_build_properties(
        build_properties)

    assert expected == current


@pt.inlineCallbacks
def test_get_last_trigger_properties():
    class Stub(steps.ReduceTriggerProperties):
        # {buildrequestid: [buildid, buildid]}
        buildrequests = {1: [1, 2],
                         2: [3, 4]}

        # {buildid: {propName: (propValue, desc)}}
        builds = {1: {'key1': ('value1', 'desc1'),
                      'key2': ('value2', 'desc2')},
                  2: {'key3': ('value3', 'desc3'),
                      'key4': ('value4', 'desc4')},
                  3: {'key5': ('value5', 'desc5'),
                      'key6': ('value6', 'desc6')},
                  4: {'key7': ('value7', 'desc7'),
                      'key8': ('value8', 'desc8')}}

        def get_last_step_build_requests(self):
            return list(self.buildrequests.keys())

        def get_buildrequest_builds(self, buildrequestid):
            return self.buildrequests[buildrequestid]

        def get_build_properties(self, buildid):
            return self.builds[buildid]

    step = Stub(reducefn=lambda:None)
    current = yield step.get_previous_trigger_properties()

    expected = [{k: v[0] for k, v in prop.items()}
                for prop in Stub.builds.values()]

    assert current == expected


@pt.inlineCallbacks
def test_run():
    o1, o2, o3 = object(), object(), object()

    class Stub(steps.ReduceTriggerProperties):
        # self.setProperty(k, v, self.name, runtime=True)
        setProperty = Mock()

        def get_previous_trigger_properties(self):
            return [{"key1": "value1", "key2": "value2"},
                    {"key3": "value3", "key4": "value4"}]

    mock = Mock()
    mock.return_value = {"key1": "value1", "key2": "value2",
                         "key3": "value3", "key4": "value4"}

    step = Stub(reducefn=mock)

    result = yield step.run()

    mock.assert_called_once_with(*step.get_previous_trigger_properties())

    for key, value in mock.return_value.items():
        step.setProperty.assert_any_call(
            key, value, step.name, runtime=True)

    assert result is results.SUCCESS
