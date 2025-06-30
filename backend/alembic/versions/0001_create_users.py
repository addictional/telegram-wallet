"""create users table"""

from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('telegram_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('username', sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table('users')
