"""channels table constraint keys

Revision ID: e511d62f38b7
Revises: 8efbde3ecaeb
Create Date: 2019-12-06 10:33:42.532924

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'e511d62f38b7'
down_revision = '8efbde3ecaeb'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("channels") as batch_op:
        batch_op.create_foreign_key("fk_channels_bouquets",
                                    "bouquets", ["bouquet_id"], ["id"],
                                    ondelete='CASCADE')
    with op.batch_alter_table("channels") as batch_op:
        batch_op.create_unique_constraint("uk_calendar_id",
                                          ["calendar_id"])


def downgrade():
    with op.batch_alter_table("channels") as batch_op:
        batch_op.drop_constraint("fk_channels_bouquets", type_='foreignkey')
    with op.batch_alter_table("channels") as batch_op:
        batch_op.drop_constraint("uk_calendar_id", type_='unique')
