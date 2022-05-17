"""UserPicture unique user_id fk added.

Revision ID: 6a176094c31c
Revises: bfe8b82b590e
Create Date: 2022-05-12 11:16:43.506493

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6a176094c31c'
down_revision = 'bfe8b82b590e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user-pictures', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user-pictures', type_='unique')
    # ### end Alembic commands ###