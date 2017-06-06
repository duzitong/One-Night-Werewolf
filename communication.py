from server import gameServer
from utilities import DEBUG


def getInput(pid, decription = ''):
    if DEBUG:
        return input(decription)
    else:
        return gameServer.get_selection_from_client(pid, decription)

def sendOutput(pid, message):
    if DEBUG:
        print(message)
    else:
        gameServer.send_message(pid, message)

def broadcast(message):
    if DEBUG:
        print(message)
    else:
        gameServer.broadcast(message)
