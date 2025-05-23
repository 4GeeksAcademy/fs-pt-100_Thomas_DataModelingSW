"""empty message

Revision ID: 9111aa7e9b4f
Revises: 73eae43a76fe
Create Date: 2025-05-15 13:43:36.200253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9111aa7e9b4f'
down_revision = '73eae43a76fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('profiles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('bio', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='profiles_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='profiles_pkey')
    )
    op.drop_table('favorites')
    # ### end Alembic commands ###
