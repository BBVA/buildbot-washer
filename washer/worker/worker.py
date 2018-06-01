import os

from buildbot_worker.bot import Worker
from environconfig import EnvironConfig, StringVar, IntVar, PathVar, BooleanVar
from twisted.application import service
from twisted.scripts._twistd_unix import UnixApplicationRunner, ServerOptions
import netifaces


GATEWAY = netifaces.gateways()["default"][netifaces.AF_INET][0]

print(os.environ)

class BuildbotConf(EnvironConfig):
    """
    Environment variable configuration.

    """
    BUILDMASTER = StringVar(default=GATEWAY)
    BUILDMASTER_PORT = IntVar(default=9989)
    WORKERNAME = StringVar(default="example-worker")
    WORKERPASS = StringVar(default="pass")
    BASEDIR = PathVar(default=os.path.abspath(os.path.dirname(__file__)))
    KEEPALIVE = IntVar(default=600)
    MAXDELAY = IntVar(default=300)


class WasherConf(EnvironConfig):
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


if __name__ == '__main__':

    del os.environ["LD_LIBRARY_PATH"]
    del os.environ["PYTHONHOME"]

    InlineApplication(OPTIONS).run()
