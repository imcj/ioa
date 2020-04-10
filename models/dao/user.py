import utils
from ..tables import UserTable
from .database_access_object import DatabaseAccessObject


class UserDAO(DatabaseAccessObject):

    async def register(self, user):
        salt = utils.rand()

        user['password'] = utils.hash(user['password'], salt)
        user['salt'] = salt

        result = await self.connection.execute(UserTable.insert().values(**user))
        user['id'] = result.lastrowid

        return user

    async def find_by_username(self, username: str):
        query = await self.connection.execute(UserTable.select(
            UserTable.c.username == username)
        )
        user = await query.fetchone()
        return user

    async def find(self, id: int):
        query = await self.connection.execute(UserTable.select(
            UserTable.c.id == id)
        )
        user = await query.fetchone()
        return user
