
import logging
from ..tables import TopicTable, UserTable
from sqlalchemy.orm.util import aliased
from sqlalchemy.sql import select
from .database_access_object import DatabaseAccessObject
from sqlalchemy import text, Integer, Text, desc, func

class TopicDAO(DatabaseAccessObject):

    logger : logging.Logger = logging.getLogger("TopicDAO")

    async def create(self, topic):
        result = await self.connection.execute(TopicTable.insert().values(**topic))
        topic['id'] = result.lastrowid
        return topic

    async def edit(self, topic_id : int, topic):
        await self.connection.execute(
            TopicTable.update()
                .where(TopicTable.c.id==topic_id)
                .values(
                    title=topic['title'], 
                    content=topic['content'], 
                    # updated_at=text('NOW()')
                )
        )


    async def find(self, id):
        query = await self.connection.execute(TopicTable.select(TopicTable.c.id == id))
        return await query.fetchone()

    async def view_increase(self, topic_id : int):

        statement = """UPDATE topics 
            SET view_count = view_count + 1
            WHERE id = %d""" % (topic_id,)
    
        return await self.connection.execute(statement)


    async def find_topics(self, page : int):
    
        lastReplyAlias = aliased(UserTable)

        query = await self.connection.execute(
            select(
                [
                    TopicTable, 
                    UserTable.c.username,
                    lastReplyAlias.c.username.label("last_replied_by_username"),
                ],
                TopicTable.c.deleted_at == None
            ).select_from(
                TopicTable.outerjoin(
                    UserTable, TopicTable.c.author_id == UserTable.c.id
                )
                .outerjoin(lastReplyAlias, TopicTable.c.last_replied_by_user_id == lastReplyAlias.c.id)
            )
            .order_by(desc(TopicTable.c.last_replied_at))
            .limit(50)
            .offset((page - 1) * 50)
        )
        topics = await query.fetchall()
        return topics

    async def count(self):
        query = await self.connection.execute(select([func.count(TopicTable.c.id).label("count")]))
        row = await query.fetchone()
        return row['count']
    
    async def reply_by(self, author_id, topic_id : int):

        statement = """UPDATE topics 
            SET reply_count = reply_count + 1,
                last_replied_at = NOW(),
                last_replied_by_user_id = %d 
            WHERE id = %d""" % (topic_id, topic_id,)
    
        return await self.connection.execute(statement)

    async def delete(self, topic_id : int):
        return await self.connection.execute(
            TopicTable
                .update()
                .where(TopicTable.c.id == topic_id)
                .values(deleted_at=text('NOW()'))
        )