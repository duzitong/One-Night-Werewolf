import cmd
import pickle
import socket
import threading


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
        except (BrokenPipeError, ConnectionResetError):
            pass
        self.cleanup

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
    client = User(socket.create_connection(('localhost', 19420)), 'dubeat')
    client.start()