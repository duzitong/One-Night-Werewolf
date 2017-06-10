import traceback


def retry(action):
    def retryTillSuccess(*args):
        failed = True
        while failed:
            try:
                return action(*args)
                failed = False
            except Exception as e:
                traceback.print_exc()
                failed = True
    return retryTillSuccess
