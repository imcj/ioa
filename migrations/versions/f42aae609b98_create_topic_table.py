"""create topic table

Revision ID: f42aae609b98
Revises: 447720762b73
Create Date: 2019-12-07 15:42:14.501356

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, Text, Integer


# revision identifiers, used by Alembic.
revision = 'f42aae609b98'
down_revision = '447720762b73'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'topics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(1000)),
        sa.Column('content', Text),
        sa.Column('author_id', sa.Integer),
        sa.Column('reply_count', sa.Integer, server_default=('0')),
        sa.Column('view_count', sa.Integer, server_default=text('0')),
        sa.Column('created_at', sa.DateTime, server_default=text('NOW()')),
        sa.Column('last_replied_at', sa.DateTime, server_default=text('NOW()')),
        sa.Column('last_replied_by_user_id', Integer),
    )

    op.create_table(
        'replies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('content', Text),
        sa.Column('author_id', sa.Integer),
        sa.Column('topic_id', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=text('NOW()')),
    )


def downgrade():
    pass
