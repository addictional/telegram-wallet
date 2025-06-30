from alembic import op
import sqlalchemy as sa

revision = '0001_create_users'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False, unique=True, index=True),
        sa.Column('first_name', sa.String(length=100)),
        sa.Column('last_name', sa.String(length=100)),
        sa.Column('username', sa.String(length=100)),
    )

def downgrade():
    op.drop_table('users')
