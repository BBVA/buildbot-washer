"""
Environconfig classes for the worker.

These classes allow the worker to easily reach the environment variables.

"""
import os

from environconfig import EnvironConfig, StringVar, IntVar, PathVar, BooleanVar


class Buildbot(EnvironConfig):
    """Buildbot environment variable."""
    BUILDMASTER = StringVar(default="127.0.0.1")
    BUILDMASTER_PORT = IntVar(default=9989)
    WORKERNAME = StringVar(default="example-worker")
    WORKERPASS = StringVar(default="pass")
    BASEDIR = PathVar(default=os.path.abspath(os.path.dirname(__file__)))
    KEEPALIVE = IntVar(default=600)
    MAXDELAY = IntVar(default=300)


class Washer(EnvironConfig):
    """Washer environment variable."""

    __varprefix__ = "WASHER_"

    FORCE_GATEWAY = BooleanVar(default=False)
    LOG_FILE = StringVar(default="-")
    DAEMON = BooleanVar(default=False)
