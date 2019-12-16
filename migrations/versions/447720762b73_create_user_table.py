"""create user table

Revision ID: 447720762b73
Revises: 
Create Date: 2019-12-07 15:37:24.358402

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '447720762b73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('password', sa.String(256)),
        sa.Column('salt', sa.String(16)),
        sa.Column('created_at', sa.DateTime, server_default=text('NOW()')),
        sa.Column('updated_at', sa.DateTime, server_default=text('NOW()')),
    )
    op.create_index('username_idx', 'users', ['username'])
    op.create_index('email_idx', 'users', ['email'])


def downgrade():
    pass
