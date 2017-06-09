import random
from gameTypes import *
import threading
from server import gameServer
import time
from collections import Counter
import traceback


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
    del players[:]
    del remainings[:]
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
    votes = gameServer.get_votes(localize('VOTE'), len(players))
    for i, player in enumerate(players):
        sendOutput(i, localize('YOUR_FINAL_IDENTITY').format(player))
    frequency = Counter(votes.values())
    if len(frequency) == len(players):
        for player in players:
            if isinstance(player, Werewolf):
                broadcast(localize('WEREWOLF_WIN'))
                break
        else:
            broadcast(localize('MAN_WIN'))
    else:
        for i in range(1, len(frequency)):
            if len(set([countTuple[1] for countTuple in frequency.most_common(i)])) != 1:
                check_identities(frequency.most_common(i-1))
                break
        else:
            check_identities(frequency.most_common(len(frequency)))

def check_identities(counter):
    manWin = False
    others = []
    for pid in [countTuple[0] for countTuple in counter]:
        if isinstance(players[pid], Hunter):
            others.append(players[pid].kill_another(votes))
        elif isinstance(players[pid], Werewolf):
            manWin = True
        else:
            pass
    if not manWin:
        for other in others:
            if isinstance(players[other], Werewolf):
                manWin = True
    broadcast(localize('MAN_WIN') if manWin else localize('WEREWOLF_WIN'))
        

if __name__ == '__main__':
    t = ServerThread()
    t.start()
    while True:
        try:
            input('Wait for players...')
            if gameServer.get_client_count() <= 10:
                gameServer.broadcast_players()
                startGame(gameServer.get_client_count())
                for player in players:
                    print(str(player))
                input('Gaming...')
                endGame()
        except Exception as e:
            traceback.print_exc()
