"""Add JAMB score and admission status

Revision ID: 8fdd7e025fb4
Revises: c803c35b5e23
Create Date: 2026-09-11 20:06:21.783572

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8fdd7e025fb4"
down_revision = "c803c35b5e23"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("students", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "admission_status",
                sa.String(length=30),
                nullable=False,
                server_default="Undecided"
            )
        )


def downgrade():

    with op.batch_alter_table("students", schema=None) as batch_op:

        batch_op.drop_column("admission_status")