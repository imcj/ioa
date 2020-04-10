import utils
from models import UserDAO, CredentailInvalid
from .exceptions import DuplicatedUser
from ioa import transaction


class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    @transaction()
    async def register(self, user):

        found = await self.user_dao.find_by_username(user['username'])
        if found:
            raise DuplicatedUser(user['username'])

        return await self.user_dao.register(user)

    async def login(self, cridentail):
        user = await self.user_dao.find_by_username(cridentail['username'])

        if user:
            if utils.hash(cridentail['password'], user['salt']) == user['password']:
                return user

        raise CredentailInvalid()
