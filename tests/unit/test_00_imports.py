import pytest


def test_worker_command():
    try:
        from washer.worker.commands import WasherCommand
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
