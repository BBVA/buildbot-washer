from functools import singledispatch
from collections.abc import Iterable, Mapping


@singledispatch
def recursiverender(obj, callback):
    if hasattr(obj, 'getRenderingFor'):
        return callback(obj)
    else:
        return obj


@recursiverender.register(str)
def _(obj, callback):
    return obj


@recursiverender.register(Iterable)
def _(obj, callback):
    return obj.__class__(recursiverender(o, callback) for o in obj)


@recursiverender.register(Mapping)
def _(obj, callback):
    return obj.__class__((k, recursiverender(v, callback))
                         for k, v in obj.items())
