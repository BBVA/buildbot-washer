"""
Configure and launch the worker.

Options are passed via environment variables.

"""
from buildbot_worker.bot import Worker
from twisted.application import service
from twisted.scripts._twistd_unix import UnixApplicationRunner, ServerOptions

from . import commands, conf


try:
    import netifaces
except ImportError:
    GATEWAY = None
else:
    GATEWAY = netifaces.gateways()["default"][netifaces.AF_INET][0]


def prepare_app():
    """
    Prepare a worker application containing the custom washer commands and that
    can be run without the use of the `buildbot` command script.

    """
    application = service.Application('buildbot-worker')
    master = (GATEWAY
              if conf.Washer.FORCE_GATEWAY
              else conf.Buildbot.BUILDMASTER)
    worker = Worker(master,
                    conf.Buildbot.BUILDMASTER_PORT,
                    conf.Buildbot.WORKERNAME,
                    conf.Buildbot.WORKERPASS,
                    conf.Buildbot.BASEDIR,
                    conf.Buildbot.KEEPALIVE,
                    umask=None,
                    maxdelay=conf.Buildbot.MAXDELAY,
                    numcpus=None,
                    allow_shutdown=None,
                    maxRetries=None)
    worker.setServiceParent(application)

    class InlineApplication(UnixApplicationRunner):
        def createOrGetApplication(self):
            nonlocal application
            return application

    options = ServerOptions()
    options["nodaemon"] = not conf.Washer.DAEMON
    options["logfile"] = conf.Washer.LOG_FILE

    commands.register()

    return InlineApplication(options)
