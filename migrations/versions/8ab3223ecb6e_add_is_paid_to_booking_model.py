"""add is_paid to booking model

Revision ID: 8ab3223ecb6e
Revises: 7061651c5b80
Create Date: 2024-10-31 11:43:55.097077

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8ab3223ecb6e"
down_revision = "7061651c5b80"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("is_paid", sa.Boolean(), server_default="false", nullable=False)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.drop_column("is_paid")

    # ### end Alembic commands ###
