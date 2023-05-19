"""empty message

Revision ID: 75b927c6ffbb
Revises: 521561c2b87f
Create Date: 2023-05-18 10:54:23.630645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75b927c6ffbb'
down_revision = '521561c2b87f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=265), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.alter_column('latitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.alter_column('latitude',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)

    op.drop_table('admin')
    # ### end Alembic commands ###