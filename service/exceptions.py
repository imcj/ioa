class DuplicatedUser(Exception):
    username : str = None

    def __init__(self, username):
        self.username = username
        super().__init__("has %s" % username)

class NoPermission(Exception):
    pass

class NotFound(Exception):
    pass