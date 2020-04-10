import sqlalchemy as sa
from sqlalchemy import text, Text, Integer

meta = sa.MetaData()
UserTable = sa.Table('users', meta,
                     sa.Column('id', sa.Integer, primary_key=True),
                     sa.Column('username', sa.String(255)),
                     sa.Column('email', sa.String(255)),
                     sa.Column('password', sa.String(256)),
                     sa.Column('salt', sa.String(16)),
                     sa.Column('created_at', sa.DateTime, server_default=text('NOW()')),
                     sa.Column('updated_at', sa.DateTime, server_default=text('NOW()')),
                     )

TopicTable = sa.Table('topics', meta,
                      sa.Column('id', sa.Integer, primary_key=True),
                      sa.Column('title', sa.String(1000)),
                      sa.Column('content', Text),
                      sa.Column('author_id', sa.Integer),
                      sa.Column('reply_count', sa.Integer),
                      sa.Column('view_count', sa.Integer),
                      sa.Column('created_at', sa.DateTime, server_default=text('NOW()')),
                      sa.Column('last_replied_at', sa.DateTime, server_default=text('NOW()')),
                      sa.Column('last_replied_by_user_id', Integer),
                      sa.Column('deleted_at', sa.DateTime, default=None),
                      )

ReplyTable = sa.Table('replies', meta,
                      sa.Column('id', sa.Integer, primary_key=True),
                      sa.Column('content', Text),
                      sa.Column('author_id', sa.Integer),
                      sa.Column('topic_id', sa.Integer),
                      sa.Column('created_at', sa.DateTime, server_default=text('NOW()')),
                      sa.Column('updated_at', sa.DateTime, server_default=text('NOW()')),
                      )
