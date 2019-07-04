from washer.master.recursiverender import recursiverender
from buildbot.process.properties import Property, Secret

import pytest


def test_nonrecursive_rendering():
    # recursiverender(<object>, <callback>)
    obj = Property('foo')

    def callback(irenderable):
        return irenderable

    assert recursiverender(obj, callback) is obj


def test_recursiverendering_calls_callback_if_renderable():
    obj = Property('foo')

    was_called = False

    def callback(irenderable):
        nonlocal was_called
        was_called = True

    recursiverender(obj, callback)

    assert was_called


def test_recursiverendering_dont_call_callback_if_not_renderable():
    obj = object()

    was_called = False

    def callback(irenderable):
        nonlocal was_called
        was_called = True

    recursiverender(obj, callback)

    assert not was_called


@pytest.mark.parametrize("obj", [
    (Property('foo'), "NotAProperty"),
    [Property('foo'), "NotAProperty"],
    {'foo': Property('foo'), 'bar': "NotAProperty"}])
def test_simplestruct_nested_rendering(obj):
    was_called = False

    def callback(irenderable):
        nonlocal was_called
        was_called = True
        assert irenderable == Property("foo")
        return irenderable

    assert recursiverender(obj, callback) == obj
    assert was_called


def test_complexstruct_nested_rendering():
    obj = [{'foo1': (Property('foo'), Secret('bar')),
            'bar1': {'foo': 'foo', 'bar': Property('bar')}},
           {'foo2': (Property('foo'), Secret('bar')),
            'bar2': {'foo': 'foo', 'bar': Property('bar')}}]
    expected = [{'foo1': (None, None),
                 'bar1': {'foo': 'foo', 'bar': None}},
                {'foo2': (None, None),
                 'bar2': {'foo': 'foo', 'bar': None}}]

    def callback(irenderable):
        return None

    assert recursiverender(obj, callback) == expected
