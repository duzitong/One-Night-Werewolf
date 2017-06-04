import pickle
import queue
import select
import socketserver
import threading
from utilities import retry


class GameServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, request_handler_class):
        super().__init__(server_address, request_handler_class, True)
        self.clients = []

    def add_client(self, client):
        if client not in self.clients:
            self.clients.append(client)

    def broadcast(self, message):
        for client in self.clients:
            client.schedule(message)

    def remove_client(self, client):
        self.clients.remove(client)

    def send_message(self, playerId, message):
        self.clients[playerId].schedule(message)

    def get_selection_from_client(self, playerId, description):
        self.clients[playerId].getResponse(description)

    def get_votes(self, description):
        results = {}
        vthreads = []
        for i, client in enumerate(self.clients):
            vt = VoteThread(client, description, results, i)
            vthreads.append(vt)
            vt.start()
        for vt in vthreads:
            vt.join()
        return results

    def get_clients(self):
        return self.clients


class IOHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.buffer = queue.Queue()
        super().__init__(request, client_address, server)

    def setup(self):
        super().setup()
        self.server.add_client(self)
        print('{} entered'.format(self.name))

    def handle(self):
        try:
            while True:
                self.empty_buffers()
        except (ConnectionResetError, EOFError):
            self.finish()

    def empty_buffers(self):
        while not self.buffer.empty():
            pickle.dump(self.buffer.get_nowait(), self.wfile)

    @property
    def readable(self):
        return self.connection in select.select(
            (self.connection,), (), (), 0.1)[0]

    @property
    def name(self):
        return self.connection.getpeername()

    def schedule(self, message):
        self.buffer.put_nowait(('print', message))
    
    def getResponse(self, description):
        self.buffer.put_nowait(('input', description))
        while True:
            if self.readable:
                message = pickle.load(self.rfile)
                print(message)
                return message

    def finish(self):
        self.server.remove_client(self)
        print('{} exited'.format(self.name))
        super().finish()


class VoteThread(threading.Thread):
    def __init__(self, client, description, results, pid):
        self.client = client
        self.description = description
        self.results = results
        self.pid = pid

    @retry
    def run(self):
        self.results[self.pid] = int(self.client.getResponse(self.description))


gameServer = GameServer(('localhost', 19420), IOHandler)