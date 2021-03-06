"""CASCADE delete added to m2m models in charity>charity_employee>charity_employee_roles.

Revision ID: 532f289d1900
Revises: e5ca5459a7fb
Create Date: 2022-06-21 13:21:38.446685

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '532f289d1900'
down_revision = 'e5ca5459a7fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('charity_employee_association_charity_id_fkey', 'charity_employee_association', type_='foreignkey')
    op.drop_constraint('charity_employee_association_employee_id_fkey', 'charity_employee_association', type_='foreignkey')
    op.create_foreign_key(None, 'charity_employee_association', 'employees', ['employee_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'charity_employee_association', 'charities', ['charity_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('charity_employee_role_association_charity_employee_id_fkey', 'charity_employee_role_association', type_='foreignkey')
    op.drop_constraint('charity_employee_role_association_role_id_fkey', 'charity_employee_role_association', type_='foreignkey')
    op.create_foreign_key(None, 'charity_employee_role_association', 'charity_employee_association', ['charity_employee_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'charity_employee_role_association', 'employee_roles', ['role_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'charity_employee_role_association', type_='foreignkey')
    op.drop_constraint(None, 'charity_employee_role_association', type_='foreignkey')
    op.create_foreign_key('charity_employee_role_association_role_id_fkey', 'charity_employee_role_association', 'employee_roles', ['role_id'], ['id'])
    op.create_foreign_key('charity_employee_role_association_charity_employee_id_fkey', 'charity_employee_role_association', 'charity_employee_association', ['charity_employee_id'], ['id'])
    op.drop_constraint(None, 'charity_employee_association', type_='foreignkey')
    op.drop_constraint(None, 'charity_employee_association', type_='foreignkey')
    op.create_foreign_key('charity_employee_association_employee_id_fkey', 'charity_employee_association', 'employees', ['employee_id'], ['id'])
    op.create_foreign_key('charity_employee_association_charity_id_fkey', 'charity_employee_association', 'charities', ['charity_id'], ['id'])
    # ### end Alembic commands ###
