def swap(x, y):
    x, y = y, x


class Identity(object):
    def __init__(self, players, remainings):
        self.players = players
        self.remainings = remainings

    def __str__(self):
        return self.__class__.__name__

    def action(self):
        raise NotImplementedError(self.action)


class Werewolf(Identity):
    def isBad():
        return True


class Man(Identity):
    def isBad():
        return False


class Doppelganger(Man):
    def action(self):
        try:
            r = int(input('Select one identity in the remainings: '))
            print(self.remainings[r])
            p = int(input('Give this identity to one player: '))
            swap(self.players[p], self.remainings[r])
        except Exception as e:
            print('Failure, ignored action')


class Minion(Identity):
    pass

class Mason(Man):
    pass

class Seer(Man):
    pass

class Robber(Man):
    pass

class Troublemaker(Man):
    pass

class Drunk(Man):
    pass

class Insomniac(Man):
    pass

class Hunter(Man):
    pass

class Villager(Man):
    pass

class Tanner(Man):
    pass
