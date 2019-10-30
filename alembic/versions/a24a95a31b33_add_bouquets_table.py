"""add bouquets table

Revision ID: a24a95a31b33
Revises: ffc544c2bbe6
Create Date: 2019-10-30 16:02:06.763172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a24a95a31b33'
down_revision = 'ffc544c2bbe6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bouquets',
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('date_updated', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bouquet_name', sa.String(), nullable=True),
    sa.Column('refresh_url', sa.String(), nullable=False),
    sa.Column('should_refresh', sa.Boolean(), nullable=True),
    sa.Column('api_key1', sa.String(), nullable=False),
    sa.Column('api_key2', sa.String(), nullable=False),
    sa.Column('auth_credentials', sa.String(), nullable=False),
    sa.Column('state', sa.Enum('active', 'archived', 'deleted', name='statetype'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channels',
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('date_updated', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.String(), nullable=False),
    sa.Column('calendar_id', sa.String(), nullable=False),
    sa.Column('resource_id', sa.String(), nullable=False),
    sa.Column('extra_atrributes', sa.String(), nullable=False),
    sa.Column('bouquet_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.Enum('active', 'archived', 'deleted', name='statetype'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('channels')
    op.drop_table('bouquets')
    # ### end Alembic commands ###
