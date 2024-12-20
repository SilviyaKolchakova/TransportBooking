"""add vehicle relationship in booking model

Revision ID: c8d6354b6246
Revises: 8ab3223ecb6e
Create Date: 2024-11-08 23:37:49.691908

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c8d6354b6246"
down_revision = "8ab3223ecb6e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.add_column(sa.Column("vehicle_pk", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, "vehicles", ["vehicle_pk"], ["pk"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("vehicle_pk")

    # ### end Alembic commands ###
