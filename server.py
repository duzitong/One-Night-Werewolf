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
        return self.clients[playerId].getResponse(description)

    def get_votes(self, description):
        results = {}
        vthreads = []
        for i, client in enumerate(self.clients):
            vt = VoteThread(client, description, results, i, self.get_client_count())
            vthreads.append(vt)
            vt.start()
        for vt in vthreads:
            vt.join()
        return results

    def get_client_count(self):
        return len(self.clients)

    def broadcast_players(self):
        nicknames = '\n'.join(['{}: {}'.format(i, client.nickname) for i, client in enumerate(self.clients)])
        self.broadcast(nicknames)


class IOHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.buffer = queue.Queue()
        super().__init__(request, client_address, server)

    def setup(self):
        super().setup()
        self.server.add_client(self)
        self.nickname = self.getNicknameFromPeer()
        print('{}:{} entered'.format(self.nickname, self.name))

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
                return message

    def getNicknameFromPeer(self):
        while True:
            if self.readable:
                nickname = pickle.load(self.rfile)
                return nickname

    def finish(self):
        self.server.remove_client(self)
        print('{} exited'.format(self.name))
        super().finish()


class VoteThread(threading.Thread):
    def __init__(self, client, description, results, pid, limit):
        self.client = client
        self.description = description
        self.results = results
        self.pid = pid
        self.limit = limit
        super(VoteThread, self).__init__()

    @retry
    def run(self):
         vote = int(self.client.getResponse(self.description))
         assert vote < self.limit
         self.results[self.pid] = vote

gameServer = GameServer(('0.0.0.0', 19420), IOHandler)
