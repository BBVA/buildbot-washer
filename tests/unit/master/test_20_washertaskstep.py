from unittest import mock

from twisted.internet import defer
import pytest_twisted as pt

from washer.master import steps
from washer.master import remotecommand


def test_defaults():
    step = steps.WasherTask()
    assert step.name == 'WasherTask'
    assert step.haltOnFailure is True
    assert step.flunkOnFailure is True
    assert step.useProgress is True
    assert "task_name" in step.renderables
    assert "task_args" in step.renderables


def test_task_name():
    step = steps.WasherTask(task_name="mytask")
    assert step.task_name == "mytask"


def test_task_args():
    step = steps.WasherTask(task_args={"foo": "bar"})
    assert step.task_args == {"foo": "bar"}


@pt.inlineCallbacks
def test_run_use_WasherTaskCommand():
    with mock.patch('buildbot.process.buildstep.LoggingBuildStep.run'):
        with mock.patch('washer.master.steps.WasherTask.addLog'):
            step = steps.WasherTask(task_name="mytask", task_args={"foo": "bar"})

            step.checkWorkerHasCommand = mock.MagicMock()

            step.runCommand = mock.MagicMock()
            step.runCommand.side_effect = lambda *_, **__: defer.returnValue(0)

            yield step.run()

            step.checkWorkerHasCommand.assert_called_once_with("washertask")

            assert len(step.runCommand.mock_calls) == 1
            call = step.runCommand.mock_calls[0]

            # check for first arg
            assert isinstance(call[1][0], remotecommand.WasherTaskCommand)
