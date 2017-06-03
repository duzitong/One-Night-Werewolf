from utilities import *
from localization import localize


class Identity(object):
    def __init__(self, players, remainings):
        self.players = players
        self.remainings = remainings

    def __str__(self):
        return self.__class__.__name__

    def action(self):
        raise NotImplementedError(self.action)

    def setId(self, pid):
        self.pid = pid


class Werewolf(Identity):
    def isBad(self):
        return True


class Man(Identity):
    def isBad(self):
        return False


class Witch(Man):
    @retry
    def action(self):
        r = getInput(self.pid, localize('WITCH_LOOK'))
        sendOutput(self.pid, localize('WITCH_SELECTED').format(self.remainings[r]))
        p = getInput(self.pid, localize('WITCH_GIVE'))
        swap(self.players[p], self.remainings[r])


class Minion(Identity):
    def action(self):
        wolves = []
        for i, player in enumerate(self.players):
            if isinstance(player, Werewolf):
                wolves.append(i)
        if wolves:
            sendOutput(self.pid, localize('MINION_PARTNER').format(wolves))
        else:
            sendOutput(self.pid, localize('MINION_NO_PARTNER'))

class Mason(Man):
    def action(self):
        partner = None
        for i, player in enumerate(self.players):
            if isinstance(player, Mason) and player is not self:
                partner = i
        if partner:
            sendOutput(self.pid, localize('Mason_PARTNER').format(partner))
        else:
            sendOutput(self.pid, localize('Mason_NO_PARTNER'))

class Seer(Man):
    @retry
    def action(self):
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

class SeniorWerewolf(Werewolf):
    pass

class JuniorWerewolf(Werewolf):
    pass
