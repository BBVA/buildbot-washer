from functools import singledispatch
from collections.abc import Iterable, Mapping
from twisted.internet import defer


@singledispatch
@defer.inlineCallbacks
def recursiverender(obj, callback):
    if hasattr(obj, 'getRenderingFor'):
        return (yield callback(obj))
    else:
        return (yield obj)


@recursiverender.register(str)
@defer.inlineCallbacks
def _(obj, callback):
    return (yield obj)


@recursiverender.register(Iterable)
@defer.inlineCallbacks
def _(obj, callback):
    result = []
    for o in obj:
        result.append((yield recursiverender(o, callback)))

    return obj.__class__(result)


@recursiverender.register(Mapping)
@defer.inlineCallbacks
def _(obj, callback):
    result = []
    for k, v in obj.items():
        result.append((k, (yield recursiverender(v, callback))))

    return obj.__class__(result)
