from unittest.mock import patch

from washer.worker.commands import WasherTask
from washer.worker.commands import washertask


def test_washertask_register_task():
    def mytask():
        pass

    with patch.dict(WasherTask._tasks, {}):
        newtask = washertask(mytask)  # Equivalent to decorate the function
        assert newtask is mytask
        assert WasherTask._tasks.get("mytask", None) is mytask
