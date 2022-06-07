"""CharityOrganisation 'description' field non unique.

Revision ID: cc7757c0f971
Revises: 874af5e5e316
Create Date: 2022-05-27 10:54:26.128561

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cc7757c0f971'
down_revision = '874af5e5e316'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('CharityOrganisations_description_key', 'CharityOrganisations', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('CharityOrganisations_description_key', 'CharityOrganisations', ['description'])
    # ### end Alembic commands ###
