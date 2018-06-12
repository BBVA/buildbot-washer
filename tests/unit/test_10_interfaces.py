import abc

import pytest

from buildbot import plugins
from buildbot.process import buildstep
from buildbot.process.remotecommand import RemoteCommand
from buildbot.steps.worker import CompositeStepMixin
from buildbot_worker.commands.base import Command

from washer.worker import commands
from washer.worker import actions
from washer.master import remotecommand
from washer.master import steps


def test_worker_command_is_command():
    assert issubclass(commands.WasherTask, Command)


@pytest.mark.parametrize(
    "subaction",
    actions.MasterAction.__subclasses__())
def test_actions_are_MasterAction_and_tuple(subaction):
    assert issubclass(subaction, actions.MasterAction)
    assert issubclass(subaction, tuple)


def test_MasterAction_is_abstract():
    assert isinstance(actions.MasterAction, abc.ABCMeta)


def test_MasterAction_message_is_abstractproperty():
    assert "message" in actions.MasterAction.__abstractmethods__


@pytest.mark.parametrize(
    "attribute,value",
    [("requiredArgs", ["task_name", "task_args"]), ])
def test_WasherTask_attributes(attribute, value):
    assert getattr(commands.WasherTask, attribute, object()) == value


def test_WasherTaskCommand_is_RemoteCommand():
    assert issubclass(remotecommand.WasherTaskCommand, RemoteCommand)


def test_TriggerFromFile_is_Trigger_and_CompositeStepMixin():
    assert issubclass(steps.TriggerFromFile, plugins.steps.Trigger)
    assert issubclass(steps.TriggerFromFile, CompositeStepMixin)


def test_steps_WasherTask_is_LoggingBuildStep_and_CompositeStepMixin():
    assert issubclass(steps.WasherTask, buildstep.LoggingBuildStep)
    assert issubclass(steps.WasherTask, CompositeStepMixin)
