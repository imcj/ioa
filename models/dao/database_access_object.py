
from aiomysql.sa import SAConnection

class DatabaseAccessObject:
    connection : SAConnection

    def __init__(self, connection : SAConnection):
        self.connection = connection