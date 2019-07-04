import pytest


def test_import_recursiverender():
    try:
        from washer.master.recursiverender import recursiverender
    except ImportError as exc:
        assert False, exc
