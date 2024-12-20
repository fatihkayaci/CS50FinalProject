"""Initial migration

Revision ID: db0e866378ab
Revises: 76080035d6c3
Create Date: 2024-12-17 16:10:31.338850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db0e866378ab'
down_revision = '76080035d6c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media_tbl', schema=None) as batch_op:
        batch_op.alter_column('page_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True,
               existing_server_default=sa.text("('')"))

    with op.batch_alter_table('text_tbl', schema=None) as batch_op:
        batch_op.add_column(sa.Column('page_name', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('text_tbl', schema=None) as batch_op:
        batch_op.drop_column('page_name')

    with op.batch_alter_table('media_tbl', schema=None) as batch_op:
        batch_op.alter_column('page_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False,
               existing_server_default=sa.text("('')"))

    # ### end Alembic commands ###
