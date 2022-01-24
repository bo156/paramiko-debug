import paramiko
from paramiko.client import SSHClient
from .config import SSH_SERVER_PORT, SSH_SERVER_PASSWORD, SSH_SERVER_IP, SSH_SERVER_USERANME


def get_ssh_client(ip=SSH_SERVER_IP, port=SSH_SERVER_PORT, username=SSH_SERVER_USERANME, password=SSH_SERVER_PASSWORD):
    # type: (str, int, str, str) -> SSHClient
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy)
    client.connect(ip, port=port, username=username, password=password)
    return client


def run_command_with_exec_command(client, command):
    # type: (SSHClient, str) -> str
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode().strip()

def run_command_with_shell(client, command):
    # type: (SSHClient, str) -> str
    shell = client.invoke_shell()
    while shell.recv_ready():
        shell.recv(1024)  # Read base output
    shell.send(command.encode())
    # result = b''
    # while shell.recv_ready():
    result = shell.recv(1024)
    return result

