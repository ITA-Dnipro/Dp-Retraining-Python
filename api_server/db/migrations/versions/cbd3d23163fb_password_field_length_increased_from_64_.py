"""'password' field length increased from 64 to 256 ch.

Revision ID: cbd3d23163fb
Revises: dfeca01e8726
Create Date: 2022-04-30 12:39:42.267902

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cbd3d23163fb'
down_revision = 'dfeca01e8726'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'password',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=256),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'password',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
    # ### end Alembic commands ###
