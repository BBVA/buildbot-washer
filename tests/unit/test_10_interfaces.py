import abc

import pytest
from buildbot_worker.commands.base import Command

from washer.worker import commands
from washer.worker import actions


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
    [("requiredArgs", ["task"]), ])
def test_WasherTask_attributes(attribute, value):
    assert getattr(commands.WasherTask, attribute, object()) == value
