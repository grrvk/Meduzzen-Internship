"""initial commit

Revision ID: 94e1d3c7dd86
Revises: 
Create Date: 2023-09-24 18:30:38.591166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94e1d3c7dd86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('User',
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('user_email', sa.String(), nullable=False),
            sa.Column('user_firstname', sa.String(), nullable=False),
            sa.Column('user_lastname', sa.String(), nullable=False),
            sa.Column('user_status', sa.String(), nullable=True),
            sa.Column('user_city', sa.String(), nullable=True),
            sa.Column('user_phone', sa.String(), nullable=True),
            sa.Column('user_avatar', sa.String(), nullable=True),
            sa.Column('hashed_password', sa.String(), nullable=False),
            sa.Column('is_superuser', sa.Boolean(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.Column('email', sa.String(length=320), nullable=False),
            sa.Column('is_active', sa.Boolean(), nullable=False),
            sa.Column('is_verified', sa.Boolean(), nullable=False),
            sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_User_email'), 'User', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index(op.f('ix_User_email'), table_name='User')
    op.drop_table('User')
    # ### end Alembic commands ###
