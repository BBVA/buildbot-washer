from collections import namedtuple
import abc


def withfields(*fields):
    """Returns an "anonymous" namedtuple with *fields."""
    return namedtuple("Fields", fields)


class MasterAction(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def message(self):  # pragma: no cover
        """
        Return a valid dictionary to be passed to `Command.sendStatus`.

        """
        pass


class UpdateProgress(MasterAction, withfields("name", "value")):
    @property
    def message(self):
        return {"progress": {self.name: self.value}}


class UpdateSummary(MasterAction, withfields("value")):
    @property
    def message(self):
        return {"summary": self.value}


class CreateNamedLog(MasterAction, withfields("name")):
    @property
    def message(self):
        return {"createlog": self.name}


class AppendToLog(MasterAction, withfields("name", "value")):
    @property
    def message(self):
        return {"log": (self.name, self.value)}


class AppendStdout(MasterAction, withfields("value")):
    @property
    def message(self):
        return {"stdout": self.value}


class AppendStderr(MasterAction, withfields("value")):
    @property
    def message(self):
        return {"stderr": self.value}


class AppendHeader(MasterAction, withfields("value")):
    @property
    def message(self):
        return {"header": self.value}


class Warn(MasterAction, withfields("value")):
    @property
    def message(self):
        return {"log": ("warnings", self.value)}
