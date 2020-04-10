class CredentailInvalid(Exception):
    pass


from .dao.reply import ReplyDAO
from .dao.topic import TopicDAO
from .dao.user import UserDAO
from .tables import *
