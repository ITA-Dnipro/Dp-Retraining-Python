"""change_charity_fields_to_unique

Revision ID: 5ec0f3ad9936
Revises: c70d4140c86f
Create Date: 2022-05-25 14:16:02.437078

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5ec0f3ad9936'
down_revision = 'c70d4140c86f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'CharityOrganisations', ['phone_number'])
    op.create_unique_constraint(None, 'CharityOrganisations', ['organisation_email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'CharityOrganisations', type_='unique')
    op.drop_constraint(None, 'CharityOrganisations', type_='unique')
    # ### end Alembic commands ###
