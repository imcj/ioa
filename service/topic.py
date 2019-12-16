import bleach
from models import (
    TopicDAO,
    ReplyDAO,
    UserDAO,
)
from . import Service
from .exceptions import NoPermission, NotFound


class TopicService(Service):
    
    async def topics(self, page : int):
        async with self.engine.acquire() as connection:
            topic_dao = TopicDAO(connection)
            topics = await topic_dao.find_topics(page)
            count = await topic_dao.count()
        return {
            "topics": topics,
            "count": count,
        }

    async def speak(self, topic, user_id : int):
        topic['author_id'] = user_id
        topic['last_replied_by_user_id'] = user_id

        async with self.engine.acquire() as connection:
            topic_dao = TopicDAO(connection)

            transaction = await connection.begin()
            topic = await topic_dao.create(topic)
            await transaction.commit()

        return topic

    async def edit(self, topic_id : int, user_id : int, topic):
        async with self.engine.acquire() as connection:
            topic_dao = TopicDAO(connection)

            transaction = await connection.begin()
            found = await topic_dao.find(topic_id)
            await topic_dao.edit(topic_id, topic)
            await transaction.commit()
            return topic

    async def shutup(self, topic_id : int, user_id : int):
        async with self.engine.acquire() as connection:
            topic_dao = TopicDAO(connection)
            transaction = await connection.begin()
            topic = await topic_dao.find(topic_id)
            
            if topic['author_id'] != user_id:
                await transaction.rollback()
                raise NoPermission()

            if topic:
                await topic_dao.delete(topic_id)
            await transaction.commit()
        
        return topic

    async def detail(self, id : int, page : int):
        async with self.engine.acquire() as connection:
            topic_dao = TopicDAO(connection)
            reply_dao = ReplyDAO(connection)
            user_dao = UserDAO(connection)

            
            topic = self.row2dict(await topic_dao.find(id))
            topic['replies'] = await reply_dao.find_by_topic_id(id, page)
            topic['author'] = await user_dao.find(topic['author_id'])
            topic['replies_count'] = (await reply_dao.count_by_topic_id(id))['count']
            topic['last_comment_by'] = await user_dao.find(topic['last_replied_by_user_id'])

            transaction = await connection.begin()
            await topic_dao.view_increase(id)
            await transaction.commit()

        return topic

    async def reply(self, reply, user_id : int):
        reply['author_id'] = user_id

        async with self.engine.acquire() as connection:
            transaction = await connection.begin()

            topic_dao = TopicDAO(connection)
            reply_dao = ReplyDAO(connection)
            reply = await reply_dao.create(reply)
            await topic_dao.reply_by(reply["author_id"], reply["topic_id"])

            await transaction.commit()
            
        return reply