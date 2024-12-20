"""Initial migration

Revision ID: 48037247bf38
Revises: 5b807ed81c3b
Create Date: 2024-12-18 17:46:29.301884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48037247bf38'
down_revision = '5b807ed81c3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tblfoods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('page_name', sa.String(length=50), nullable=False),
    sa.Column('photopath', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('text', sa.String(length=5000), nullable=True),
    sa.Column('order_index', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tblmedia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=100), nullable=True),
    sa.Column('page_name', sa.String(length=50), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tbltext',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photoid', sa.Integer(), nullable=True),
    sa.Column('id_name', sa.String(length=50), nullable=False),
    sa.Column('text', sa.String(length=5000), nullable=True),
    sa.ForeignKeyConstraint(['photoid'], ['tblmedia.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbltext')
    op.drop_table('tblmedia')
    op.drop_table('tblfoods')
    # ### end Alembic commands ###
