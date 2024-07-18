"""Money is int

Revision ID: 2ffcd037033a
Revises: 092458eaaefe
Create Date: 2024-07-18 11:04:49.476354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ffcd037033a'
down_revision: Union[str, None] = '092458eaaefe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'balance',
               existing_type=sa.NUMERIC(precision=2, scale=0),
               type_=sa.Integer(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'balance',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(precision=2, scale=0),
               existing_nullable=False)
    # ### end Alembic commands ###
