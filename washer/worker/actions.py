from collections import namedtuple
import abc


__all__ = ["UpdateProgress", "UpdateSummary", "CreateNamedLog", "AppendToLog",
           "AppendStdout", "AppendStderr", "AppendHeader", "Warn"]


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
    """Update the progress `name` to the new value `value`."""
    @property
    def message(self):
        return {"progress": {self.name: self.value}}


class UpdateSummary(MasterAction, withfields("value")):
    """Update the summary with `value`."""
    @property
    def message(self):
        return {"summary": self.value}


class CreateNamedLog(MasterAction, withfields("name")):
    """Create a new log named `name`."""
    @property
    def message(self):
        return {"createlog": self.name}


class AppendToLog(MasterAction, withfields("name", "value")):
    """Append `value` to the log named `name`."""
    @property
    def message(self):
        return {"log": (self.name, self.value)}


class AppendStdout(MasterAction, withfields("value")):
    """Add the message `value` as stdout to the *stdio* log."""
    @property
    def message(self):
        return {"stdout": self.value}


class AppendStderr(MasterAction, withfields("value")):
    """Add the message `value` as stderr to the *stdio* log."""
    @property
    def message(self):
        return {"stderr": self.value}


class AppendHeader(MasterAction, withfields("value")):
    """Add the message `value` as a header to the *stdio* log."""
    @property
    def message(self):
        return {"header": self.value}


class Warn(MasterAction, withfields("value")):
    """
    Add the message `value` to the *warnings* log.

    .. note::

       The use of this action will mark the *washertask* and, even if it finish
       successfully the result will  have a warning.

    """
    @property
    def message(self):
        return {"log": ("warnings", self.value)}


class SetProperty(MasterAction, withfields("name", "value")):
    @property
    def message(self):
        return {"property": (self.name, self.value)}
