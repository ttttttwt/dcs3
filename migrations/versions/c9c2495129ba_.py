"""empty message

Revision ID: c9c2495129ba
Revises: e59c2f6ab05a
Create Date: 2023-05-13 19:53:15.158045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9c2495129ba'
down_revision = 'e59c2f6ab05a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actives', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('speed', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actives', schema=None) as batch_op:
        batch_op.drop_column('speed')
        batch_op.drop_column('time')

    # ### end Alembic commands ###
