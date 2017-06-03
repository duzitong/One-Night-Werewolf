translation = {
    'WITCH_LOOK': {
        'en': 'Select one identity in the remainings: '
    },
    'WITCH_SELECTED': {
        'en': 'Selected identity is: {}'
    },
    'WITCH_GIVE': {
        'en': 'Give this identity to one player: '
    },
    'MINION_PARTNER': {
        'en': 'Your partners are: {}'
    },
    'MINION_NO_PARTNER': {
        'en': 'Your have no partner'
    },
    'Mason_PARTNER': {
        'en': 'Your partner is: {}'
    },
    'Mason_NO_PARTNER': {
        'en': 'Your have no partner'
    },
}

location = 'en'

def localize(key):
    return translation[key.upper()][location]
