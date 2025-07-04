"""Add is_default for DayVariant

Revision ID: 18ede4529cb0
Revises: 07424ad5dd29
Create Date: 2025-06-15 12:49:13.659516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18ede4529cb0'
down_revision = '07424ad5dd29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('day_variant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_default', sa.Boolean(), server_default='False', nullable=False))
        batch_op.create_index('only_one_default_variant', ['day_id', 'is_default'], unique=True, postgresql_where='is_default')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('day_variant', schema=None) as batch_op:
        batch_op.drop_index('only_one_default_variant', postgresql_where='is_default')
        batch_op.drop_column('is_default')

    # ### end Alembic commands ###
