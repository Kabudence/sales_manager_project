"""Initial migration

Revision ID: de067e2eb7fe
Revises: 
Create Date: 2024-12-26 11:47:07.409113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de067e2eb7fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('linea_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_producto_linea', 'linea', ['linea_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.drop_constraint('fk_producto_linea', type_='foreignkey')
        batch_op.drop_column('linea_id')

    # ### end Alembic commands ###
