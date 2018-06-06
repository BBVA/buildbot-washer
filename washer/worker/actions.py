from collections import namedtuple
import abc


def WithFields(*fields):
    """Returns an "anonymous" namedtuple with *fields."""
    return namedtuple("Fields", fields)


class MasterAction(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def message(self):
        """
        Return a valid dictionary to be passed to `Command.sendStatus`.

        """
        pass


class UpdateProgress(MasterAction,
                     WithFields("name", "value")):
    """
#     @property
#     def message(self):
#         return {"progress": {self.name: self.value}}
    """
    pass


class UpdateSummary(MasterAction, tuple):
    pass


class CreateNamedLog(MasterAction, tuple):
    pass


class AppendToLog(MasterAction, tuple):
    pass


class AppendStdout(MasterAction, tuple):
    pass


class AppendStderr(MasterAction, tuple):
    pass


class AppendHeader(MasterAction, tuple):
    pass
