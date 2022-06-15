"""FundraiseStatus name field now unique.

Revision ID: 90c56cd024b2
Revises: 04dff00d60a9
Create Date: 2022-06-14 16:54:27.062659

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '90c56cd024b2'
down_revision = '04dff00d60a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'fundraise_statuses', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fundraise_statuses', type_='unique')
    # ### end Alembic commands ###
