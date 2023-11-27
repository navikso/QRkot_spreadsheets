"""User

Revision ID: 868b285113c6
Revises: 1103655b1077
Create Date: 2023-11-11 18:46:58.028635

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "868b285113c6"
down_revision = "1103655b1077"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column("first_name", existing_type=sa.VARCHAR(), nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column("first_name", existing_type=sa.VARCHAR(), nullable=False)

    # ### end Alembic commands ###
