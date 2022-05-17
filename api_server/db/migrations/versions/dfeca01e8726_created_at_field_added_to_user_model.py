"""'created_at' field added to User model.

Revision ID: dfeca01e8726
Revises: 8c6984b95f60
Create Date: 2022-04-30 10:45:25.843644

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dfeca01e8726'
down_revision = '8c6984b95f60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'created_at')
    # ### end Alembic commands ###
