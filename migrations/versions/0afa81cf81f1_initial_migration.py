"""Initial migration

Revision ID: 0afa81cf81f1
Revises: cb1f4f437f14
Create Date: 2024-12-16 20:35:41.068203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0afa81cf81f1'
down_revision = 'cb1f4f437f14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media_tbl', schema=None) as batch_op:
        batch_op.add_column(sa.Column('index', sa.Integer(), nullable=False))
        batch_op.drop_column('order')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media_tbl', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order', sa.INTEGER(), nullable=True))
        batch_op.drop_column('index')

    # ### end Alembic commands ###