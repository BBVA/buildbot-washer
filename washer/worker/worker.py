"""
Configure and launch the worker.

Options are passed via environment variables.

"""
import os
from collections import namedtuple
from functools import partial

import invoke

from twisted.internet import threads, defer
from buildbot_worker.bot import Worker
from buildbot_worker.commands.registry import commandRegistry
from buildbot_worker.commands.base import Command
from environconfig import EnvironConfig, StringVar, IntVar, PathVar, BooleanVar
from twisted.application import service
from twisted.scripts._twistd_unix import UnixApplicationRunner, ServerOptions
import netifaces
from twisted.internet import reactor


GATEWAY = netifaces.gateways()["default"][netifaces.AF_INET][0]


class BuildbotConf(EnvironConfig):
    """
    Buildbot environment variable.

    """
    BUILDMASTER = StringVar(default=GATEWAY)
    BUILDMASTER_PORT = IntVar(default=9989)
    WORKERNAME = StringVar(default="example-worker")
    WORKERPASS = StringVar(default="pass")
    BASEDIR = PathVar(default=os.path.abspath(os.path.dirname(__file__)))
    KEEPALIVE = IntVar(default=600)
    MAXDELAY = IntVar(default=300)


class WasherConf(EnvironConfig):
    """
    Washer environment variable.

    """
    __varprefix__ = "WASHER_"

    FORCE_GATEWAY = BooleanVar(default=False)
    LOG_FILE = StringVar(default="-")
    DAEMON = BooleanVar(default=False)


APPLICATION = service.Application('buildbot-worker')
MASTER = GATEWAY if WasherConf.FORCE_GATEWAY else BuildbotConf.BUILDMASTER
WORKER = Worker(MASTER,
                BuildbotConf.BUILDMASTER_PORT,
                BuildbotConf.WORKERNAME,
                BuildbotConf.WORKERPASS,
                BuildbotConf.BASEDIR,
                BuildbotConf.KEEPALIVE,
                umask=None,
                maxdelay=BuildbotConf.MAXDELAY,
                numcpus=None,
                allow_shutdown=None,
                maxRetries=None)
WORKER.setServiceParent(APPLICATION)


class InlineApplication(UnixApplicationRunner):
    def createOrGetApplication(self):
        global APPLICATION
        return APPLICATION


OPTIONS = ServerOptions()
OPTIONS["nodaemon"] = not WasherConf.DAEMON
OPTIONS["logfile"] = WasherConf.LOG_FILE


RemoteLog = namedtuple('RemoteLog', ['log', 'message'])


class StdioLog(RemoteLog):
    pass


Progress = namedtuple('Progress', ['name', 'value'])
Summary = namedtuple('Summary', ['message'])

StdoutLog = partial(StdioLog, "stdout")
StderrLog = partial(StdioLog, "stderr")
HeaderLog = partial(StdioLog, "header")


def user_script(ctx, cfg):
    from time import sleep
    yield HeaderLog("Starting process...")
    yield RemoteLog("ojete", "nianonianoniano")
    with ctx.cd("/tmp"):
        lines = ctx.run("ls -1").stdout.splitlines()

        for idx, filename in enumerate(lines, 1):
            yield Progress("files", idx)
            yield RemoteLog(filename, "Test test test!")
            yield Summary("%d file(s) processed" % idx)
            yield HeaderLog("Filename found %r" % filename)
            if ctx.run("test -f %s" % filename,
                       warn=True,
                       hide=True).exited == 0:
                yield StdoutLog(filename)
            else:
                yield StderrLog(filename)
            sleep(1)
    return 0


class WasherRun(Command):
    header = "washer"

    @defer.inlineCallbacks
    def start(self):
        def something_long():
            events = user_script(invoke.context.Context(), {})
            while True:
                try:
                    event = next(events)
                except StopIteration as exc:
                    # exc.value is the return value
                    return exc.value
                else:
                    if isinstance(event, RemoteLog):
                        if isinstance(event, StdioLog):
                            reactor.callFromThread(
                                self.sendStatus,
                                {event.log: event.message + "\n"})
                        else:
                            # Send message to master
                            reactor.callFromThread(
                                self.sendStatus,
                                {"log": (event.log, event.message + "\n")})
                    elif isinstance(event, Progress):
                        reactor.callFromThread(
                            self.sendStatus,
                            {"progress": {event.name: event.value}})
                    elif isinstance(event, Summary):
                        reactor.callFromThread(
                            self.sendStatus,
                            {"summary": event.message})
                    else:
                        raise RuntimeError(
                            "Unknown event type %r" % type(event))

        d = threads.deferToThread(something_long)

        def cb(status):
            self.sendStatus({"rc": status})

        def eb(f):
            self.sendStatus({"stderr": f.getTraceback()})
            self.sendStatus({"rc": -2})

        d.addCallbacks(cb, eb)

        yield d


commandRegistry["washer"] = WasherRun


if __name__ == '__main__':

    # TODO: Add list of to-be-restored variables as cmdline parameters.
    os.environ.pop("LD_LIBRARY_PATH", None)
    os.environ.pop("PYTHONHOME", None)

    InlineApplication(OPTIONS).run()
