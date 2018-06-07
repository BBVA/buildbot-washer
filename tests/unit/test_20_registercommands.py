from unittest.mock import patch

from buildbot_worker.commands import registry
import pytest

from washer.worker import commands


@pytest.mark.parametrize("command", [commands.WasherTask])
def test_commands_register(command):
    with patch.dict(registry.commandRegistry, {}):
        commands.register()
        assert registry.commandRegistry.get(command._name, None) is command
