#!/usr/bin/env python

import socket
import json

# This is an example of a UDP client - it creates
# a socket and sends data through it

# create the UDP socket
import sys


def run_command(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

    data = json.dumps({'command': 'run', 'script': command}).encode('utf-8')

    # Simply set up a target address and port ...
    addr = ('127.0.0.1', 7777)
    # ... and send data out to it!
    sock.sendto(data, addr)

    data, server = sock.recvfrom(4096)
    data = json.loads(data.decode('utf-8'))

    return data['id']

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Call: ./run.py <command to run>')
    else:
        tid = run_command(sys.argv[1])
        print("Runned as task = {}".format(tid))