class User:
    id : int = None
    username : str = None

    def is_anonymous(self):
        return False

class AnonymousUser:
    def is_anonymous(self):
        return True