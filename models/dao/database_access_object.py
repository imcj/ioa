import ioa
from aiomysql.sa import SAConnection


class DatabaseAccessObject:
    connection: SAConnection

    def __init__(self):
        connection = ioa.connection_context.get()
        self.connection = connection
