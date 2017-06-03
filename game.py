import random
from gameTypes import *
import threading
from server import gameServer


players = []
remainings = []


class ServerThread(threading.Thread):
    def run(self):
        gameServer.serve_forever()


def startGame(n):
    allIdentities = [Witch(players, remainings) for i in range(n + 3)]
    random.shuffle(allIdentities)
    for i in range(n):
        players.append(allIdentities[i])
        players[i].setId(i)
    for i in range(n, n+3):
        remainings.append(allIdentities[i])

    steps = [Witch]
    for step in steps:
        for player in allIdentities[:n]:
            if isinstance(player, step):
                player.action()

def end():
    pass

if __name__ == '__main__':
    t = ServerThread()
    t.start()
    while True:
        input('Wait for players...')
        if len(gameServer.get_clients) == 10:
            startGame(10)
            break
