"""EmailConfirmationToken user_id non unique field.

Revision ID: fdcbb010ccba
Revises: c8d4ed070b9f
Create Date: 2022-05-19 16:25:45.785101

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fdcbb010ccba'
down_revision = 'c8d4ed070b9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('email-confirmation-token_user_id_key', 'email-confirmation-token', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('email-confirmation-token_user_id_key', 'email-confirmation-token', ['user_id'])
    # ### end Alembic commands ###