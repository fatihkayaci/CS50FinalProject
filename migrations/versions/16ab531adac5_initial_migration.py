"""Initial migration

Revision ID: 16ab531adac5
Revises: 48037247bf38
Create Date: 2024-12-18 19:33:53.776256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16ab531adac5'
down_revision = '48037247bf38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tblmediaandtext',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('page_name', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('path', sa.String(length=50), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.Column('text1', sa.String(length=5000), nullable=True),
    sa.Column('text2', sa.String(length=5000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('tblmedia')
    op.drop_table('tbltext')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbltext',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('photoid', sa.INTEGER(), nullable=True),
    sa.Column('id_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('text', sa.VARCHAR(length=5000), nullable=True),
    sa.ForeignKeyConstraint(['photoid'], ['tblmedia.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tblmedia',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('path', sa.VARCHAR(length=50), nullable=False),
    sa.Column('label', sa.VARCHAR(length=100), nullable=True),
    sa.Column('page_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('file_name', sa.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('tblmediaandtext')
    # ### end Alembic commands ###
