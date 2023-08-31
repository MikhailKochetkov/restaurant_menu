"""change models

Revision ID: c56855554923
Revises: cb34f56f0f71
Create Date: 2023-08-31 22:23:05.884038

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c56855554923'
down_revision: str | None = 'cb34f56f0f71'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'dishes', ['title'])
    op.create_unique_constraint(None, 'submenus', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'submenus', type_='unique')
    op.drop_constraint(None, 'dishes', type_='unique')
    # ### end Alembic commands ###
