"""empty message

Revision ID: 521561c2b87f
Revises: c9c2495129ba
Create Date: 2023-05-17 12:07:51.380685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '521561c2b87f'
down_revision = 'c9c2495129ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('longitude', sa.Float()))
        batch_op.drop_column('distance')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('distance', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
        batch_op.drop_column('longitude')

    # ### end Alembic commands ###
