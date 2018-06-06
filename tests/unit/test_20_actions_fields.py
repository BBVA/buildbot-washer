import pytest

from washer.worker import actions


@pytest.mark.wip
@pytest.mark.parametrize(
    "subaction,fields",
    [(actions.UpdateProgress, ["name", "value"]), ])
def test_actions_fields(subaction, fields):
    assert set(subaction._fields) == set(fields)
