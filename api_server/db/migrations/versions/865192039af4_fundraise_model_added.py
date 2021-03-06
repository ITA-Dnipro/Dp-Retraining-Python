"""Fundraise model added.

Revision ID: 865192039af4
Revises: b5651a776b42
Create Date: 2022-06-10 07:04:32.261504

"""
from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '865192039af4'
down_revision = 'b5651a776b42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fundraisers',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('charity_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=512), nullable=False),
    sa.Column('description', sa.String(length=8192), nullable=False),
    sa.Column('goal', sa.Numeric(precision=20, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('ending_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['charity_id'], ['CharityOrganisations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fundraisers_id'), 'fundraisers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_fundraisers_id'), table_name='fundraisers')
    op.drop_table('fundraisers')
    # ### end Alembic commands ###
