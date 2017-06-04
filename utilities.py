from server import gameServer

DEBUG = False

def swap(x, y):
    x, y = y, x

def retry(action):
    def retryTillSuccess(*args):
        failed = True
        while failed:
            try:
                action(*args)
                failed = False
            except Exception as e:
                print('Error, try again!\n{}'.format(str(e)))
                failed = True
    return retryTillSuccess

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
