import bleach
from models import (
    TopicDAO,
    ReplyDAO,
    UserDAO,
)
from .exceptions import NoPermission, NotFound
from ioa import transaction, serializer


class TopicService:

    def __init__(self):
        self.topic_dao = TopicDAO()
        self.reply_dao = ReplyDAO()

    async def topics(self, page: int):
        topic_list = await self.topic_dao.find_topics(page)
        count = await self.topic_dao.count()
        return {
            "topics": topic_list,
            "count": count,
        }

    @transaction()
    async def speak(self, topic, user_id: int):
        topic['author_id'] = user_id
        topic['last_replied_by_user_id'] = user_id

        topic = await self.topic_dao.create(topic)

        return topic

    @transaction()
    async def edit(self, topic_id: int, user_id: int, topic):
        await self.topic_dao.edit(topic_id, topic)

    @transaction()
    async def shutup(self, topic_id: int, user_id: int):
        topic = await self.topic_dao.find(topic_id)

        if topic['author_id'] != user_id:
            raise NoPermission()

        if topic:
            await self.topic_dao.delete(topic_id)

        return topic

    @transaction()
    async def detail(self, id: int, page: int):
        topic_dao = TopicDAO()
        reply_dao = ReplyDAO()
        user_dao = UserDAO()

        topic = serializer.serialize(await topic_dao.find(id))
        topic['replies'] = await reply_dao.find_by_topic_id(id, page)
        topic['author'] = await user_dao.find(topic['author_id'])
        topic['replies_count'] = (await reply_dao.count_by_topic_id(id))['count']
        topic['last_comment_by'] = await user_dao.find(topic['last_replied_by_user_id'])

        await topic_dao.view_increase(id)

        return topic

    @transaction()
    async def reply(self, reply, user_id: int):
        reply['author_id'] = user_id

        reply = await self.reply_dao.create(reply)
        await self.topic_dao.reply_by(reply["author_id"], reply["topic_id"])
        return reply
