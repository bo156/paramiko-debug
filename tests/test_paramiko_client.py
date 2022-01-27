import pytest
from _pytest.fixtures import fixture
from paramiko.client import SSHClient

from paramiko_client.paramilo_client import get_ssh_client, run_command_with_exec_command, run_command_with_shell, \
    run_wrapped_command_in_shell


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


@pytest.mark.parametrize('command, expected_result', [('echo hello\n', 'hello')])
def test_shell(ssh_client, command, expected_result):
    # type: (SSHClient, str, str) -> None
    result = run_command_with_shell(ssh_client, command)
    assert result == expected_result


@pytest.mark.parametrize('command, expected_result', [
    ('echo hello', 'hello'),
    ('ls -la /tmp || exit 1', "total 52\n" 
"drwxrwxrwt 13 root root 4096 Jan 27 12:10 .\n"
"drwxr-xr-x 20 root root 4096 Jan 27 09:09 ..\n"
"drwxrwxrwt  2 root root 4096 Jan 27 09:13 .font-unix\n"
"drwxrwxrwt  2 root root 4096 Jan 27 09:13 .ICE-unix\n"
"drwx------  3 root root 4096 Jan 27 09:13 snap.docker\n"
"drwx------  3 root root 4096 Jan 27 09:13 snap.lxd\n"
"drwx------  3 root root 4096 Jan 27 09:13 systemd-private-ed9a78d64ec2407c9f43265e6c36e3c5-systemd-logind.service-GWDzLi\n"
"drwx------  3 root root 4096 Jan 27 09:13 systemd-private-ed9a78d64ec2407c9f43265e6c36e3c5-systemd-resolved.service-s5Izkg\n"
"drwx------  3 root root 4096 Jan 27 09:13 systemd-private-ed9a78d64ec2407c9f43265e6c36e3c5-systemd-timesyncd.service-PtEiQg\n"
"drwxrwxrwt  2 root root 4096 Jan 27 09:13 .Test-unix\n"
"drwx------  2 root root 4096 Jan 27 09:13 vmware-root_920-2731086625\n"
"drwxrwxrwt  2 root root 4096 Jan 27 09:13 .X11-unix\n"
"drwxrwxrwt  2 root root 4096 Jan 27 09:13 .XIM-unix")])
def test_wrapped_command_in_shell(command, expected_result):
    # type: (str, str) -> None
    result = run_wrapped_command_in_shell(command)
    assert result == expected_result
