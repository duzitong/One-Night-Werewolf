import random
from gameTypes import *
import threading
from server import gameServer
import time


players = []
remainings = []
WOLF_TIME = 60
MAN_TIME = 20


class ServerThread(threading.Thread):
    def run(self):
        gameServer.serve_forever()


def startGame(n):
    allIdentities = [
        JuniorWerewolf(players, remainings),
        SeniorWerewolf(players, remainings),
        Minion(players, remainings),
        Mason(players, remainings),
        Mason(players, remainings),
        Seer(players, remainings),
        Witch(players, remainings),
        Robber(players, remainings),
        Troublemaker(players, remainings),
        Drunk(players, remainings),
        Insomniac(players, remainings),
        Hunter(players, remainings),
        Hunter(players, remainings)
    ]
    random.shuffle(allIdentities)
    for i in range(n):
        players.append(allIdentities[i])
        players[i].setId(i)
    for i in range(n, n+3):
        remainings.append(allIdentities[i])

    steps = [Werewolf, Minion, Mason, Seer, Witch, Robber, Troublemaker, Drunk, Insomniac]
    for step in steps:
        btime = time.time()
        gameServer.broadcast(localize('STEP_START').format(step.__name__))
        for player in allIdentities[:n]:
            if isinstance(player, step):
                player.action()
        if step == Werewolf:
            time.sleep(max(WOLF_TIME - time.time() + btime, 0))
        elif step in [Witch, Seer, Robber, Troublemaker, Drunk]:
            time.sleep(max(MAN_TIME - time.time() + btime, 0))
        else:
            pass

def end():
    pass

if __name__ == '__main__':
    t = ServerThread()
    t.start()
    while True:
        input('Wait for players...')
        if len(gameServer.get_clients) == 10:
            startGame(10)
            input('Gaming...')
            end()
            break
