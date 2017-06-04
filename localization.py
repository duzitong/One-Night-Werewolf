translation = {
    'WITCH_LOOK': {
        'en': 'Select one identity in the remainings: '
    },
    'WITCH_SELECTED': {
        'en': 'Selected identity is: {}.'
    },
    'WITCH_GIVE': {
        'en': 'Give this identity to one player: '
    },
    'MINION_PARTNER': {
        'en': 'Your partners are: {}.'
    },
    'MINION_NO_PARTNER': {
        'en': 'Your have no partner.'
    },
    'Mason_PARTNER': {
        'en': 'Your partner is: {}.'
    },
    'Mason_NO_PARTNER': {
        'en': 'Your have no partner.'
    },
    'SEER_LOOK': {
        'en': 'Select one player to check; or Select two identites in the remainings (seperated by space): '
    },
    'SEER_CHECK_PLAYER': {
        'en': 'Player {} is {}.'
    },
    'SEER_CHECK_REMAININGS': {
        'en': 'Remaining {} is {}; Remaining {} is {}.'
    },
    'ROBBER_SELECT': {
        'en': 'Select a player to rob: '
    },
    'ROBBER_KEEP': {
        'en': 'You robbed {}'
    },
    'TROUBLEMAKER_SELECT': {
        'en': 'Select two other players to swap identity (seperated by space): '
    },
    'DRUNK_SELECT': {
        'en': 'Select one identity in the remainings: '
    },
    'INSOMNIAC_LOOK': {
        'en': 'Your final identity is {}.'
    },
    'WOLF_PARTNER': {
        'en': 'Your partner is {}.'
    },
    'ONLY_WOLF_LOOK': {
        'en': 'You are the only wolf, select one identity in the remainings: '
    },
    'ONLY_WOLF_SELECTED': {
        'en': 'Selected identity is: {}.'
    },
    'STEP_START': {
        'en': "{}'s turn..."
    },
    'VOTE': {
        'en': 'Your vote: '
    },
    'HUNTER_KILL': {
        'en': 'Vote result is {}.\nSelect one player to kill: '
    },
    'MAN_WIN': {
        'en': 'Men win! Good triumphing over evil!'
    },
    'WEREWOLF_WIN': {
        'en': 'Werewolves win! Deceive the world!'
    }
}

location = 'en'

def localize(key):
    assert key.upper in location
    return translation[key.upper()][location]
