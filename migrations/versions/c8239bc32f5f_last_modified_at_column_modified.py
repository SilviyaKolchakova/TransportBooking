"""last_modified_at column modified

Revision ID: c8239bc32f5f
Revises: 67a02b80465f
Create Date: 2024-10-20 12:59:18.989715

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c8239bc32f5f"
down_revision = "67a02b80465f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.alter_column(
            "last_modified_at", existing_type=postgresql.TIMESTAMP(), nullable=False
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.alter_column(
            "last_modified_at", existing_type=postgresql.TIMESTAMP(), nullable=True
        )

    # ### end Alembic commands ###
