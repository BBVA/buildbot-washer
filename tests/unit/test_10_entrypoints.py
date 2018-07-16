from pkg_resources import iter_entry_points

import pytest

from washer.master import steps


@pytest.mark.parametrize(
    "entrypoint,classes",
    [("buildbot.steps", [steps.TriggerFromFile,
                         steps.WasherTask,
                         steps.ReduceTriggerProperties])])
def test_entrypoints(entrypoint, classes):
    ep = [e.load() for e in iter_entry_points(entrypoint)]
    for cls in classes:
        assert cls in ep
