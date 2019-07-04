from washer.master.recursiverender import recursiverender
from buildbot.process.properties import Property, Secret

from twisted.internet import defer
import pytest_twisted as pt
import pytest


@pt.inlineCallbacks
def test_nonrecursive_rendering():
    # recursiverender(<object>, <callback>)
    obj = Property('foo')

    @defer.inlineCallbacks
    def callback(irenderable):
        return (yield irenderable)

    assert (yield recursiverender(obj, callback)) is obj


@pt.inlineCallbacks
def test_recursiverendering_calls_callback_if_renderable():
    obj = Property('foo')

    was_called = False

    @defer.inlineCallbacks
    def callback(irenderable):
        nonlocal was_called
        was_called = True
        yield None

    yield recursiverender(obj, callback)

    assert was_called


@pt.inlineCallbacks
def test_recursiverendering_dont_call_callback_if_not_renderable():
    obj = object()

    was_called = False

    @defer.inlineCallbacks
    def callback(irenderable):
        nonlocal was_called
        was_called = True
        yield None

    yield recursiverender(obj, callback)

    assert not was_called


@pytest.mark.parametrize("obj", [
    (Property('foo'), "NotAProperty"),
    [Property('foo'), "NotAProperty"],
    {'foo': Property('foo'), 'bar': "NotAProperty"}])
@pt.inlineCallbacks
def test_simplestruct_nested_rendering(obj):
    was_called = False

    @defer.inlineCallbacks
    def callback(irenderable):
        nonlocal was_called
        was_called = True
        assert irenderable == Property("foo")
        return (yield irenderable)

    assert (yield recursiverender(obj, callback)) == obj
    assert was_called


@pt.inlineCallbacks
def test_complexstruct_nested_rendering():
    obj = [{'foo1': (Property('foo'), Secret('bar')),
            'bar1': {'foo': 'foo', 'bar': Property('bar')}},
           {'foo2': (Property('foo'), Secret('bar')),
            'bar2': {'foo': 'foo', 'bar': Property('bar')}}]
    expected = [{'foo1': (None, None),
                 'bar1': {'foo': 'foo', 'bar': None}},
                {'foo2': (None, None),
                 'bar2': {'foo': 'foo', 'bar': None}}]

    @defer.inlineCallbacks
    def callback(irenderable):
        return (yield None)

    assert (yield recursiverender(obj, callback)) == expected
