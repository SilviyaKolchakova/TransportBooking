"""create booking model

Revision ID: 79af87ed1084
Revises: 958d4e4a0cb9
Create Date: 2024-10-18 14:17:14.918192

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "79af87ed1084"
down_revision = "958d4e4a0cb9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bookings",
        sa.Column("pk", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "in_progress",
                "confirmed",
                "canceled",
                "completed",
                name="bookingstatus",
            ),
            nullable=False,
        ),
        sa.Column("user_pk", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_pk"],
            ["users.pk"],
        ),
        sa.PrimaryKeyConstraint("pk"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("bookings")
    # ### end Alembic commands ###
