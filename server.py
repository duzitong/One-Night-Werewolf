import pickle
import queue
import select
import socketserver
import threading
from utilities import retry
import time

RESPONSE_TIME = 20
NICKNAME_RESPONSE_TIME = 5


class GameServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, request_handler_class):
        super().__init__(server_address, request_handler_class, True)
        self.clients = []
        self.removed = []

    def add_client(self, client):
        for info in self.removed:
            if client.name[0] == info[0]:
                self.clients[info[1]] = client
                self.removed.remove(info)
                break
        else:
            if client not in self.clients:
                self.clients.append(client)

    def broadcast(self, message):
        for client in self.clients:
            client.schedule(message)

    def remove_client(self, client):
        if client.nickname:
            self.removed.append((client.name[0], self.clients.index(client)))
            client.onFinished()
        else:
            self.clients.remove(client)

    def send_message(self, playerId, message):
        self.clients[playerId].schedule(message)

    def get_selection_from_client(self, playerId, description):
        return self.clients[playerId].getResponse(description)

    @retry
    def get_votes(self, description, length):
        results = {}
        vthreads = []
        for i, client in enumerate(self.clients[:length]):
            vt = VoteThread(client, description, results, i, self.get_client_count())
            vthreads.append(vt)
            vt.start()
        for vt in vthreads:
            vt.join()
        if len(results) != len(self.clients):
            print(results)
            raise Exception('Error')
        return results

    def get_client_count(self):
        return len(self.clients)

    def broadcast_players(self):
        nicknames = '\n'.join(['{}: {}'.format(i, client.nickname) for i, client in enumerate(self.clients)])
        self.broadcast(nicknames)


class IOHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.buffer = queue.Queue()
        self.alive = True
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
        if self.alive:
            self.buffer.put_nowait(('print', message))
    
    def getResponse(self, description, timeout=RESPONSE_TIME):
        if self.alive:
            self.buffer.put_nowait(('input', description))
            btime = time.time()
            while (time.time() - btime) < timeout:
                if self.readable and self.alive:
                    message = pickle.load(self.rfile)
                    return message
            raise Exception('Time out')

    def getNicknameFromPeer(self, timeout=NICKNAME_RESPONSE_TIME):
        btime = time.time()
        while (time.time() - btime) < timeout:
            if self.readable:
                nickname = pickle.load(self.rfile)
                self.buffer.put_nowait(('print', 'Connected. Wait for others...'))
                return nickname
        return None

    def finish(self):
        self.server.remove_client(self)
        self.alive = False
        print('{} exited'.format(self.name))

    def onFinished(self):
        super().finish()


class VoteThread(threading.Thread):
    def __init__(self, client, description, results, pid, limit):
        self.client = client
        self.description = description
        self.results = results
        self.pid = pid
        self.limit = limit
        super(VoteThread, self).__init__()

    def run(self):
        if self.client.alive:
            vote = int(self.client.getResponse(self.description))
            assert vote < self.limit
            self.results[self.pid] = vote

gameServer = GameServer(('0.0.0.0', 19420), IOHandler)
