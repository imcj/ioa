import utils
from models import UserDAO, CredentailInvalid
from . import Service
from .exceptions import DuplicatedUser

class UserService(Service):
    async def register(self, user):

        async with self.engine.acquire() as connection:
            transaction = await connection.begin()

            user_dao = UserDAO(connection)
            
            found = await user_dao.find_by_username(user['username'])
            if found:
                await transaction.rollback()
                raise DuplicatedUser(user['username'])

            user = await user_dao.register(user)

            await transaction.commit()

        return user

    async def login(self, cridentail):
        async with self.engine.acquire() as connection:
            user_dao = UserDAO(connection)
            user = await user_dao.find_by_username(cridentail['username'])

            if user:
                if utils.hash(cridentail['password'], user['salt']) == user['password']:
                    return user

        raise CredentailInvalid()