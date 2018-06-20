import pytest
from unittest import mock

from twisted.internet import reactor
from washer.worker.commands import WasherTask as WC
from washer.worker import actions
from buildbot.process import results


def fakesender(*args):
    pass


class FakeAction(actions.MasterAction):
    @property
    def message(self):
        pass


def test_do_not_accept_regular_functions_as_tasks():
    def myfunction():
        pass

    with pytest.raises(AttributeError):
        WC.runtask(fakesender, myfunction)


def test_raises_on_invalid_data():
    def mygenerator():
        yield "INVALID DATA"

    with mock.patch('twisted.internet.threads.blockingCallFromThread'):
        with pytest.raises(TypeError):
            WC.runtask(fakesender, mygenerator)


@pytest.mark.parametrize(
    "genresult,runresult",
    [(True, results.SUCCESS),
     (False, results.FAILURE)])
def test_return_value_depends_on_generator(genresult, runresult):
    def mygenerator():
        yield FakeAction()
        return genresult

    with mock.patch('twisted.internet.threads.blockingCallFromThread'):
        assert WC.runtask(fakesender, mygenerator) is runresult


@pytest.mark.parametrize("genresult", [None, object()])
def test_raise_on_invalid_return(genresult):
    def mygenerator():
        yield FakeAction()
        return genresult

    with mock.patch('twisted.internet.threads.blockingCallFromThread'):
        with pytest.raises(TypeError):
            WC.runtask(fakesender, mygenerator)


@pytest.mark.parametrize(
    "genexception",
    set(Exception.__subclasses__()) - set([StopIteration]))
def test_raise_runtimeerror_on_generator_exception(genexception):
    def mygenerator():
        yield FakeAction()
        raise genexception("This is an exception.")

    with mock.patch('twisted.internet.threads.blockingCallFromThread'):
        with pytest.raises(RuntimeError):
            WC.runtask(fakesender, mygenerator)


@pytest.mark.parametrize(
    "genresult,runresult",
    [(True, results.WARNINGS),
     (False, results.FAILURE)])
def test_return_when_warnings_are_yielded(genresult, runresult):
    def mygenerator():
        yield actions.Warn("Something happened.")
        return genresult

    with mock.patch('twisted.internet.threads.blockingCallFromThread'):
        assert WC.runtask(fakesender, mygenerator) is runresult


def test_yielded_actions_are_sent_using_callFromThread():
    class MyFakeAction(actions.MasterAction):
        message = object()

    def mygenerator():
        yield MyFakeAction()
        return True

    with mock.patch(
            'twisted.internet.threads.blockingCallFromThread') as callFromThread:
        sender = mock.Mock()
        callFromThread.side_effect = lambda _1, _2, message: sender(message)

        WC.runtask(sender, mygenerator)

        callFromThread.assert_called_once_with(reactor, sender, MyFakeAction.message)
        sender.assert_called_once_with(MyFakeAction.message)
