from server import gameServer

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
    return int(gameServer.get_selection_from_client(pid, decription))

def sendOutput(pid, message):
    gameServer.broadcast(message)
