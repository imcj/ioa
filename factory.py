import logging
from service import TopicService, UserService
from ioa.database import DatabaseContext

class ObjectFactory:

    def create_user_service(self):
        return UserService(DatabaseContext.default.engine)

    def create_topic_service(self):
        return TopicService(DatabaseContext.default.engine)

default = ObjectFactory()