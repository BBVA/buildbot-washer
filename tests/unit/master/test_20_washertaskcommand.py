from unittest import mock

from buildbot.process import results
import pytest

from washer.master import remotecommand
from washer.worker import actions


def test_defaults():
    command = remotecommand.WasherTaskCommand()
    assert command.remote_command == "washertask"
    assert command.args == {"task_name": "main", "task_args": {}}
    assert command.step is None  # Will be set on `run`.


def test_task_name():
    command = remotecommand.WasherTaskCommand(task_name="foo")
    assert command.args.get("task_name", None) == "foo"


def test_task_args():
    command = remotecommand.WasherTaskCommand(task_args={"foo": "bar"})
    assert command.args.get("task_args", None) == {"foo": "bar"}


def test_decodeRC():
    command = remotecommand.WasherTaskCommand()
    expected = {r: r for r in (results.SUCCESS,
                               results.FAILURE,
                               results.EXCEPTION,
                               results.WARNINGS)}
    assert command.decodeRC == expected


@pytest.fixture
def mockedcmd():
    command = remotecommand.WasherTaskCommand()
    command.step = mock.MagicMock()
    return command


def test_remoteupdate_UpdateProgress(mockedcmd):
    action = actions.UpdateProgress(name="myprogress", value=100)
    mockedcmd.remoteUpdate(update=action.message)

    mockedcmd.step.setProgress.assert_called_once_with("myprogress", 100)


def test_remoteupdate_UpdateSummary(mockedcmd):
    action = actions.UpdateSummary(value="mysummary")
    mockedcmd.remoteUpdate(update=action.message)

    assert mockedcmd.step.description == "mysummary"
    mockedcmd.step.updateSummary.assert_called_once_with()


def test_remoteupdate_CreateNamedLog(mockedcmd):
    mockedcmd.step.logfiles = {}

    action = actions.CreateNamedLog(name="mylog")
    mockedcmd.remoteUpdate(update=action.message)
    # addLog.. should be created once
    mockedcmd.remoteUpdate(update=action.message)

    mockedcmd.step.addLogForRemoteCommands.assert_called_once_with("mylog")


# NOTE: Append* and Warn messages are managed by super().remoteUpdate.
