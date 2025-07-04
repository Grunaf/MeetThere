"""add uuid to TripSession

Revision ID: e1eae7447da4
Revises: a7b2d50b7b86
Create Date: 2025-06-15 08:23:47.357025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1eae7447da4'
down_revision = 'a7b2d50b7b86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trip_session', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid', sa.UUID(), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_trip_session_uuid'), ['uuid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trip_session', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_trip_session_uuid'), type_='unique')
        batch_op.drop_column('uuid')

    # ### end Alembic commands ###
