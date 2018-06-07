import pytest

from washer.worker import actions


@pytest.mark.parametrize(
    "subaction,fields,message",
    [(actions.UpdateProgress, {"name": 1, "value": 2}, {"progress": {1: 2}}),
     (actions.UpdateSummary, {"value": 1}, {"summary": 1}),
     (actions.CreateNamedLog, {"name": 1}, {"createlog": 1}),
     (actions.AppendToLog, {"name": 1, "value": 2}, {"log": (1, 2)}),
     (actions.AppendStdout, {"value": 1}, {"stdout": 1}),
     (actions.AppendStderr, {"value": 1}, {"stderr": 1}),
     (actions.AppendHeader, {"value": 1}, {"header": 1}),
     (actions.Warn, {"value": 1}, {"log": ("warnings", 1)})])
def test_actions_messages(subaction, fields, message):
    assert subaction(**fields).message == message
