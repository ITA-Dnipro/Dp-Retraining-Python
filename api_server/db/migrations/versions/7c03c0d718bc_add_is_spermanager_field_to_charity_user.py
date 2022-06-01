"""add_is_spermanager_field_to_charity_user

Revision ID: 7c03c0d718bc
Revises: 5ec0f3ad9936
Create Date: 2022-05-27 08:44:42.044105

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7c03c0d718bc'
down_revision = '5ec0f3ad9936'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('charity_user_association', sa.Column('is_supermanager', sa.Boolean(), nullable=False))
    op.add_column('charity_user_association', sa.Column('is_director', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('charity_user_association', 'is_supermanager')
    op.drop_column('charity_user_association', 'is_director')
    # ### end Alembic commands ###