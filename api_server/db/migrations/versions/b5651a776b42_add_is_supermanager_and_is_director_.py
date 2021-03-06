"""add_is_supermanager_and_is_director_field_to_charity_user

Revision ID: b5651a776b42
Revises: cc7757c0f971
Create Date: 2022-06-01 18:14:05.603590

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b5651a776b42'
down_revision = 'cc7757c0f971'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('charity_user_association', sa.Column('is_supermanager', sa.Boolean(), nullable=False))
    op.add_column('charity_user_association', sa.Column('is_director', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('charity_user_association', 'is_director')
    op.drop_column('charity_user_association', 'is_supermanager')
    # ### end Alembic commands ###
