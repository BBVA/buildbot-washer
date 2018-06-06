import abc

import pytest
from buildbot_worker.commands.base import Command

from washer.worker import commands
from washer.worker import actions


@pytest.mark.wip
def test_worker_command_is_command():
    assert issubclass(commands.WasherCommand, Command)


@pytest.mark.wip
@pytest.mark.parametrize(
    "subaction",
    [actions.UpdateProgress,
     actions.UpdateSummary,
     actions.CreateNamedLog,
     actions.AppendToLog,
     actions.AppendStdout,
     actions.AppendStderr,
     actions.AppendHeader])
def test_actions_are_MasterAction_and_tuple(subaction):
    assert issubclass(subaction, actions.MasterAction)
    assert issubclass(subaction, tuple)


@pytest.mark.wip
def test_MasterAction_is_abstract():
    assert isinstance(actions.MasterAction, abc.ABCMeta)


@pytest.mark.wip
def test_MasterAction_message_is_abstractproperty():
    assert "message" in actions.MasterAction.__abstractmethods__


@pytest.mark.wip
@pytest.mark.parametrize(
    "attribute,value",
    [("requiredArgs", ["task"]), ])
def test_WasherCommand_attributes(attribute, value):
    assert getattr(commands.WasherCommand, attribute, object()) == value
