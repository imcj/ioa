
import logging
from ..tables import ReplyTable, UserTable
from sqlalchemy.orm.util import aliased
from sqlalchemy.sql import select
from sqlalchemy import text, Integer, Text, desc, func
from .database_access_object import DatabaseAccessObject

class ReplyDAO(DatabaseAccessObject):
    async def create(self, reply):
        
        result = await self.connection.execute(ReplyTable.insert().values(**reply))
        reply['id'] = result.lastrowid

        return reply

    async def find_by_topic_id(self, topic_id : int, page : int = 1):
        query = await self.connection.execute(
            select(
                [ReplyTable, UserTable.c.username]
            ).select_from(ReplyTable.join(UserTable, ReplyTable.c.author_id == UserTable.c.id))
            .where(ReplyTable.c.topic_id == topic_id)
            .limit(100)
            .offset((page - 1) * 100)
        )

        replies = await query.fetchall()
        return replies

    async def count_by_topic_id(self, topic_id : int):
        query = await self.connection.execute(
            select(
                [func.count(ReplyTable.c.id).label('count')]
            ).select_from(ReplyTable.join(UserTable, ReplyTable.c.author_id == UserTable.c.id))
            .where(ReplyTable.c.topic_id == topic_id)
        )

        replies = await query.fetchone()
        return replies