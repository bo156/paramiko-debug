import re
import time

from six import text_type
import paramiko
from paramiko.client import SSHClient
from .config import (
    SSH_SERVER_PORT,
    SSH_SERVER_PASSWORD,
    SSH_SERVER_IP,
    SSH_SERVER_USERANME,
)


def get_ssh_client(
    ip=SSH_SERVER_IP,
    port=SSH_SERVER_PORT,
    username=SSH_SERVER_USERANME,
    password=SSH_SERVER_PASSWORD,
):
    # type: (str, int, str, str) -> SSHClient
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password)
    return client


def run_command_with_exec_command(client, command):
    # type: (SSHClient, str) -> text_type
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode().strip()


def run_command_with_shell(client, command):
    # type: (SSHClient, text_type) -> text_type
    transport = client.get_transport()
    if transport is None:
        raise Exception("Invalid transport - None")
    session = transport.open_session()
    session.invoke_shell()
    while not session.recv_ready():
        time.sleep(0.5)
    _ = session.recv(65000)  # Remove beginning buffer
    session.send(command.encode())
    while not session.recv_ready():
        time.sleep(0.5)
    output = session.recv(65000)
    return output.decode().strip("\n")


def run_wrapped_command_in_shell(command):
    # type: (text_type) -> text_type
    msg = "befrwio"
    cmd_re_str = "befrwio(?P<command_res>(.*\n)*)befrwio"
    command_res_regex = re.compile(cmd_re_str)
    wrapped_command = "echo {msg};{command};echo {msg}\n".format(
        msg=msg, command=command
    )
    result = run_command_with_shell(get_ssh_client(), wrapped_command)
    real_res = command_res_regex.match(result)
    if real_res:
        return real_res.groupdict()["command_res"].strip()
    raise Exception()
