"""Add expedition_cancelled field

Revision ID: 699e07f138d7
Revises: 5064dd701bcd
Create Date: 2016-01-24 15:29:01.875788

"""

# revision identifiers, used by Alembic.
revision = '699e07f138d7'
down_revision = '5064dd701bcd'

from alembic import op
import sqlalchemy as sa


def upgrade():
### commands auto generated by Alembic - please adjust! ###
    op.alter_column('expedition', 'time_taken',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    op.add_column('fleet', sa.Column('expedition_cancelled', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fleet', 'expedition_cancelled')
    op.alter_column('expedition', 'time_taken',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    ### end Alembic commands ###