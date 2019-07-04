from unittest import mock

import pytest
import pytest_twisted as pt

from buildbot.process.properties import Property, Properties
from washer.master.steps import TriggerFromFile


def test_defaults():
    trigger = TriggerFromFile(schedulerNames=["myscheduler"])
    assert trigger.configfile == ".washer.conf"
    assert trigger.processor is None
    assert trigger.config is None
    assert "configfile" in trigger.renderables


def test_configfile():
    trigger = TriggerFromFile(schedulerNames=["myscheduler"],
                              configfile="myconfigfile")
    assert trigger.configfile == "myconfigfile"


def test_processor():
    trigger = TriggerFromFile(schedulerNames=["myscheduler"],
                              processor="myprocessor")
    assert trigger.processor == "myprocessor"


@pt.inlineCallbacks
def test_getFileContentsFromWorker():
    with mock.patch('buildbot.plugins.steps.Trigger.run'):
        trigger = TriggerFromFile(schedulerNames=["myscheduler"])

        trigger.getFileContentFromWorker = mock.MagicMock(
            return_value="content")

        yield trigger.run()

        trigger.getFileContentFromWorker.assert_called_once_with(
            trigger.configfile,
            abandonOnFailure=True)


def test_processor_is_used_in_getSchedulersAndProperties():
    called_with = None

    def myprocessor(trigger):
        nonlocal called_with
        yield {}
        called_with = trigger

    trigger = TriggerFromFile(schedulerNames=["myscheduler"],
                              processor=myprocessor)

    trigger.getSchedulersAndProperties()

    assert called_with is trigger


@pytest.mark.wip
@pt.inlineCallbacks
def test_processor_result_is_recursively_rendered_nested():
    obj = {'foo': [Property('bar'), Property('baz')],
           'bar': 'baz'}
    expected = [{'foo': ['bar', 'baz'],
                 'bar': 'baz'}]

    class FakeBuild:
        properties = Properties(foo='foo', bar='bar', baz='baz')

    def myprocessor(trigger):
        yield obj

    trigger = TriggerFromFile(schedulerNames=["myscheduler"],
                              processor=myprocessor)
    trigger.build = FakeBuild()


    result = yield trigger.getSchedulersAndProperties()

    assert result == expected

@pytest.mark.wip
@pt.inlineCallbacks
def test_processor_result_is_recursively_rendered():
    obj1 = Property('bar')
    obj2 = Property('baz')
    expected = ['bar', 'baz']

    class FakeBuild:
        properties = Properties(foo='foo', bar='bar', baz='baz')

    def myprocessor(trigger):
        yield obj1
        yield obj2

    trigger = TriggerFromFile(schedulerNames=["myscheduler"],
                              processor=myprocessor)
    trigger.build = FakeBuild()

    result = yield trigger.getSchedulersAndProperties()

    assert result == expected
