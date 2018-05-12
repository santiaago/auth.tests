'not authorized exception'

class NotAuthorizedException(Exception):
    def __init__(self, username):
        self.username = username