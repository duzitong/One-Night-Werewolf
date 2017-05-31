import random
from gameTypes import *


def start(n):
    players = []
    remainings = []
    allIdentities = [Doppelganger(players, remainings) for i in range(n + 3)]
    random.shuffle(allIdentities)
    for i in range(n):
        players.append(allIdentities[i])
    for i in range(n, n+3):
        remainings.append(allIdentities[i])

    steps = [Doppelganger]
    for step in steps:
        for player in allIdentities[:n]:
            if isinstance(player, step):
                player.action()

if __name__ == '__main__':
    start(3)
