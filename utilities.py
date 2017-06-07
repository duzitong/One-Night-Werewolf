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
