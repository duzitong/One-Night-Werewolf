from server import gameServer


def getInput(pid, decription = ''):
    return gameServer.get_selection_from_client(pid, decription)

def sendOutput(pid, message):
    gameServer.send_message(pid, message)

def broadcast(message):
    gameServer.broadcast(message)
