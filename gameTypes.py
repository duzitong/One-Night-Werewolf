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
    
    def action(self):
        wolves = []
        for i, player in enumerate(self.players):
            if isinstance(player, Werewolf) and self.pid != player.pid:
                wolves.append(i)
        if wolves:
            sendOutput(self.pid, localize('WOLF_PARTNER').format(wolves))
        else:
            self.action_only_wolf()
        if isinstance(self, SeniorWerewolf):
            self.action_senoir()

    @retry
    def action_only_wolf(self):
        r = int(getInput(self.pid, localize('ONLY_WOLF_LOOK')))
        sendOutput(self.pid, localize('ONLY_WOLF_SELECTED').format(self.remainings[r]))
    
    def action_senoir(self):
        raise NotImplementedError(self.action_senoir)

class Man(Identity):
    def isBad(self):
        return False


class Witch(Man):
    @retry
    def action(self):
        r = int(getInput(self.pid, localize('WITCH_LOOK')))
        sendOutput(self.pid, localize('WITCH_SELECTED').format(self.remainings[r]))
        p = int(getInput(self.pid, localize('WITCH_GIVE')))
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
        look = getInput(self.pid, localize('SEER_LOOK'))
        if len(look.split()) == 1:
            # check player
            sendOutput(self.pid, localize('SEER_CHECK_PLAYER').format(look, self.players[int(look)]))
        else:
            # check remainings
            r1, r2 = look.split()
            sendOutput(self.pid, localize('SEER_CHECK_REMAININGS').format(r1, self.remainings[int(r1)], r2, self.remainings[int(r2)]))


class Robber(Man):
    @retry
    def action(self):
        p = int(getInput(self.pid, localize('ROBBER_SELECT')))
        swap(self.players[self.pid], self.players[p])
        sendOutput(self.pid, localize('ROBBER_KEEP').format(self.players[self.pid]))


class Troublemaker(Man):
    @retry
    def action(self):
        p1, p2 = getInput(self.pid, localize('TROUBLEMAKER_SELECT')).split()
        if p1 == self.pid or p2 == self.pid:
            raise Exception('Self selected')
        swap(self.players[p1], self.players[p2])


class Drunk(Man):
    @retry
    def action(self):
        r = int(getInput(self.pid, localize('DRUNK_SELECT')))
        swap(self.players[self.pid], self.remainings[r])


class Insomniac(Man):
    def action(self):
        sendOutput(self.pid, localize('INSOMNIAC_LOOK').format(self.players[self.pid]))


class Hunter(Man):
    @retry
    def kill_another(self, votes):
        toKill = int(getInput(self.pid, localize('HUNTER_KILL').format(votes)))
        assert toKill < len(self.players)
        return toKill


class Villager(Man):
    pass


class Tanner(Man):
    pass


class SeniorWerewolf(Werewolf):
    @retry
    def action_senoir(self):
        p = getInput(self.pid, localize('SENIOR_WOLF_LOOK'))
        sendOutput(self.pid, localize('SENIOR_WOLF_SELECTED').format(self.players[p]))


class JuniorWerewolf(Werewolf):
    pass
