import time

from six import text_type, binary_type
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
    # type: (SSHClient, binary_type) -> text_type
    transport = client.get_transport()
    if transport is None:
        raise Exception("Invalid transport - None")
    session = transport.open_session()
    session.invoke_shell()
    while not session.recv_ready():
        time.sleep(0.5)
    _ = session.recv(65000)  # Remove beginning buffer
    session.send(command)
    output = session.recv(65000).strip()
    return output.decode()
