import pytest
from _pytest.fixtures import fixture
from paramiko.client import SSHClient

from paramiko_client.paramilo_client import get_ssh_client, run_command_with_exec_command, run_command_with_shell


@fixture
def ssh_client():
    # type: () -> SSHClient
    client = get_ssh_client()
    return client


@pytest.mark.parametrize('command, expected_result', [('echo hello', 'hello')])
def test_exec_command(ssh_client, command, expected_result):
    # type: (SSHClient, str, str) -> None
    result = run_command_with_exec_command(ssh_client, command)
    assert result == expected_result


@pytest.mark.parametrize('command, expected_result', [('echo hello', 'hello')])
def test_shell(ssh_client, command, expected_result):
    # type: (SSHClient, str, str) -> None
    result = run_command_with_shell(ssh_client, command)
    assert result == expected_result