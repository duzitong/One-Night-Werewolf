import random
from gameTypes import *
import threading
from server import gameServer
import time
from collections import Counter


players = []
remainings = []
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
WOLF_TIME = 25
MAN_TIME = 10


class ServerThread(threading.Thread):
    def run(self):
        gameServer.serve_forever()


def startGame(n):
    random.shuffle(allIdentities)
    for i in range(n):
        players.append(allIdentities[i])
        players[i].setId(i)
        sendOutput(i, localize('YOU_ARE').format(players[i]))
    for i in range(n, n+3):
        remainings.append(allIdentities[i])

    steps = [Werewolf, Minion, Mason, Seer, Witch, Robber, Troublemaker, Drunk, Insomniac]
    for step in steps:
        btime = time.time()
        broadcast(localize('STEP_START').format(step.__name__))
        for player in allIdentities[:n]:
            if isinstance(player, step):
                player.action()
        if step == Werewolf:
            time.sleep(max(WOLF_TIME - time.time() + btime, 0))
        elif step in [Witch, Seer, Robber, Troublemaker, Drunk]:
            time.sleep(max(MAN_TIME - time.time() + btime, 0))
        else:
            pass

def endGame():
    votes = gameServer.get_votes(localize('VOTE'))
    frequency = Counter(votes.values())
    manWin = False
    for i in range(1, len(frequency)):
        if len(set(Counter(frequency).most_common(i).values)) != 1:
            others = []
            for pid in Counter.most_common(i-1).keys:
                if isinstance(allIdentities[pid], Hunter):
                    others.append(allIdentities[pid].kill_another(votes))
                elif isinstance(allIdentities[pid], Werewolf):
                    manWin = True
                else:
                    pass
            break
        if not manWin:
            for other in others:
                if isinstance(allIdentities[other], Werewolf):
                    manWin = True
        broadcast(localize('MAN_WIN') if manWin else localize('WEREWOLF_WIN'))
    else:
        for player in players:
            if isinstance(player, Werewolf):
                broadcast(localize('WEREWOLF_WIN'))
                break
        else:
            broadcast(localize('MAN_WIN'))

if __name__ == '__main__':
    t = ServerThread()
    t.start()
    while True:
        try:
            input('Wait for players...')
            if gameServer.get_client_count() <= 10:
                gameServer.broadcast_players()
                startGame(gameServer.get_client_count())
                input('Gaming...')
                endGame()
        except Exception as e:
            print(e)
