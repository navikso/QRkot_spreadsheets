"""Donation migration

Revision ID: a292d0205a96
Revises: d480ea3e77c6
Create Date: 2023-11-11 16:19:39.004613

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a292d0205a96"
down_revision = "d480ea3e77c6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "donation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("full_amount", sa.Integer(), nullable=True),
        sa.Column("invested_amount", sa.Integer(), nullable=True),
        sa.Column("fully_invested", sa.Boolean(), nullable=True),
        sa.Column("create_date", sa.DateTime(), nullable=True),
        sa.Column("close_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="fk_donation_user_id_user"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("donation")
    # ### end Alembic commands ###
