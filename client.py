import pickle
import socket
import threading
import json


class User(threading.Thread):


    def __init__(self, connection, nickname):
        threading.Thread.__init__(self)
        self.connection = connection
        self.reader = connection.makefile('rb', -1)
        self.writer = connection.makefile('wb', 0)
        self.handlers = dict(print=print, input=self.forward_input)
        self.nickname = nickname
        self.alive = True

    def cleanup(self):
        self.writer.flush()
        self.connection.shutdown(socket.SHUT_RDWR)
        self.connection.close()
        self.join()

    def run(self):
        try:
            self.call(self.nickname)
            while self.alive:
                self.handle_server_command()
        except (BrokenPipeError, ConnectionResetError) as e:
            print('Connection broken...')
            raise e
        finally:
            self.cleanup()

    def handle_server_command(self):
        function, message = pickle.load(self.reader)
        self.handlers[function](message)

    def call(self, message):
        pickle.dump(message, self.writer)

    def forward_input(self, description):
        choice = input(description)
        if choice == 'exit':
            self.alive = False
        else:
            self.call(choice)


if __name__ == '__main__':
    nickname = None
    hostname = None
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            nickname = config['Nickname']
            hostname = config['Hostname']
    except Exception as e:
        print(e)
    if nickname is None:
        nickname = input('Please input your nickname: ')
    if hostname is None:
        hostname = input('Enter the host to join: ')
    client = User(socket.create_connection((hostname, 19420)), nickname)
    client.start()