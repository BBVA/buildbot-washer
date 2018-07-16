import pytest


def test_worker_command():
    try:
        from washer.worker.commands import WasherTask
    except ImportError as exc:
        assert False, str(exc)


@pytest.mark.parametrize("name", ["MasterAction",
                                  "UpdateProgress",
                                  "UpdateSummary",
                                  "CreateNamedLog",
                                  "AppendToLog",
                                  "AppendStdout",
                                  "AppendStderr",
                                  "AppendHeader",
                                  "Warn"])
def test_remote_actions(name):
    try:
        from washer.worker import actions
    except ImportError as exc:
        assert False, str(exc)
    else:
        assert hasattr(actions, name)


def test_washertask():
    try:
        from washer.worker.commands import washertask
    except ImportError as exc:
        assert False, str(exc)


def test_commands_register():
    try:
        from washer.worker.commands import register
    except ImportError as exc:
        assert False, str(exc)


def test_remotecommand_WasherTaskCommand():
    try:
        from washer.master.remotecommand import WasherTaskCommand
    except ImportError as exc:
        assert False, str(exc)


def test_steps_TriggerFromFile():
    try:
        from washer.master.steps import TriggerFromFile
    except ImportError as exc:
        assert False, str(exc)


def test_steps_WasherTask():
    try:
        from washer.master.steps import WasherTask
    except ImportError as exc:
        assert False, str(exc)


def test_steps_ReduceTriggerProperties():
    try:
        from washer.master.steps import ReduceTriggerProperties
    except ImportError as exc:
        assert False, str(exc)
