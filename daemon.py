#!/usr/bin/env python

import SocketServer as socketserver
import json
import threading
from fabric.api import execute, run
from fabric.network import disconnect_all

task_counter = 0


class UDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        data, socket = self.request
        data = json.loads(data.decode('utf-8'))
        if data.get('command') == 'run':
            global task_counter
            global queue
            with threading.Lock():
                task_id = task_counter
                task_counter += 1
            socket.sendto(json.dumps({'id': task_id}, self.client_address).encode('utf-8'), self.client_address)
            script = data.get('script')

            def runnable():
                run(script)

            execute(runnable, hosts=['localhost'])  # TODO: setup host


def main():
    try:
        server = socketserver.ThreadingUDPServer(('127.0.0.1', 7777), UDPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        disconnect_all()
    return

if __name__ == '__main__':
    main()