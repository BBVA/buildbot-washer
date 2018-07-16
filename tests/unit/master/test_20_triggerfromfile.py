from unittest import mock

import pytest_twisted as pt

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
