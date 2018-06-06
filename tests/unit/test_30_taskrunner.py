import pytest

from washer.worker.commands import WasherCommand as WC


def fake_sender():
    pass


@pytest.mark.wip
def test_runtask_do_not_accept_regular_functions_as_tasks():
    def myfunction():
        pass

    with pytest.raises(TypeError):
        WC.run_task(fake_sender, myfunction)


@pytest.mark.wip
def test_runtask_accepts_generators_as_tasks():
    def myfunction():
        yield

    try:
        # MUST NOT RAISE!
        WC.run_task(fake_sender, myfunction)
    except TypeError as exc:
        assert False, str(exc)
