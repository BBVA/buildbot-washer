from unittest import mock
from buildbot.process import results
import pytest

from washer.worker.commands import washertask, WasherTask
from washer.worker import actions

import pytest_twisted as pt


class FakeAction(actions.MasterAction):
    @property
    def message(self):
        pass


@pt.inlineCallbacks
def test_washertask_start_runs_task():
    called = False

    @washertask
    def mytask():
        nonlocal called
        yield FakeAction()
        called = True
        return True

    cmd = WasherTask(
        builder=None,
        stepId=None,
        args={"task_name": "mytask", "task_args": {}})

    yield cmd.start()

    assert called


def test_unknown_task_raise():
    with pytest.raises(RuntimeError):
        WasherTask(
            builder=None,
            stepId=None,
            args={"task_name": "foo", "task_args": {}})


@pt.inlineCallbacks
def test_washertask_expand_args():
    p1 = object()
    p2 = object()
    p3 = object()

    @washertask
    def mytask(param1, param2=None, **kwargs):
        yield FakeAction()
        assert param1 == p1
        assert param2 == p2
        assert kwargs["param3"] == p3
        return True

    cmd = WasherTask(
        builder=None,
        stepId=None,
        args={"task_name": "mytask",
              "task_args": {"param1": p1,
                            "param2": p2,
                            "param3": p3}})

    yield cmd.start()


@pt.inlineCallbacks
def test_washertask_run_in_thread():
    @washertask
    def mytask(something):
        yield FakeAction()
        return True

    myargs = {"something": True}

    cmd = WasherTask(
        builder=None,
        stepId=None,
        args={"task_name": "mytask", "task_args": myargs})

    with mock.patch('twisted.internet.threads.deferToThread') as deferToThread:
        yield cmd.start()
        deferToThread.assert_called_once_with(
            cmd.runtask,
            cmd.sendStatus,
            mytask,
            myargs)


@pytest.mark.parametrize(
    "value,warnings,message",
    [(True, True, {"rc": results.WARNINGS}),
     (True, False, {"rc": results.SUCCESS}),
     (False, True, {"rc": results.FAILURE}),
     (False, False, {"rc": results.FAILURE})])
@pt.inlineCallbacks
def test_washertask_result_status(value, warnings, message):
    @washertask
    def mytask():
        if warnings:
            yield actions.Warn("Boooo!")
        return value

    cmd = WasherTask(
        builder=None,
        stepId=None,
        args={"task_name": "mytask", "task_args": {}})

    cmd.sendStatus = mock.MagicMock()
    yield cmd.start()

    cmd.sendStatus.assert_called_with(message)


@pt.inlineCallbacks
def test_washertask_raising_task_result_status_exception():
    @washertask
    def mytask():
        yield FakeAction()
        raise ValueError("Something bad!")
        return True

    cmd = WasherTask(
        builder=None,
        stepId=None,
        args={"task_name": "mytask", "task_args": {}})

    cmd.sendStatus = mock.MagicMock()
    yield cmd.start()

    cmd.sendStatus.assert_called_with({"rc": results.EXCEPTION})
