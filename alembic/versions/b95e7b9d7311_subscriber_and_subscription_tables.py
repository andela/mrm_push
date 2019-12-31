"""subscriber and subscription tables

Revision ID: b95e7b9d7311
Revises: e511d62f38b7
Create Date: 2019-12-19 12:02:14.160467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b95e7b9d7311'
down_revision = 'e511d62f38b7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('subscribers',
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('date_updated', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscriber_name', sa.Text(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('notification_url', sa.Text(), nullable=False),
    sa.Column('subscription_method_id', sa.Integer(), nullable=True),
    sa.Column('bouquet_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['subscription_method_id'], ['subscriptions.id'], name='fk_subscribers_subscriptions', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['bouquet_id'], ['bouquets.id'], name='fk_subscribers_bouquets', onupdate='CASCADE', ondelete='CASCADE')
    ),
    op.create_table('subscriptions',
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('date_updated', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('subscribers'),
    op.drop_table('subscriptions')
