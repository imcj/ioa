"""add deleted_at field to topic table

Revision ID: 3f0496fa1b78
Revises: f42aae609b98
Create Date: 2019-12-16 17:40:32.827433

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, Text, Integer

# revision identifiers, used by Alembic.
revision = '3f0496fa1b78'
down_revision = 'f42aae609b98'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('topics', 
        sa.Column('deleted_at', sa.DateTime(), nullable=True, default=None)
    )


def downgrade():
    op.drop_column('topics', 'deleted_at',)
