"""
Initial database migration.

Creates users and todos tables.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial tables."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create todos table
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todos_id'), 'todos', ['id'], unique=False)
    op.create_index(op.f('ix_todos_user_id'), 'todos', ['user_id'], unique=False)
    op.create_index(op.f('ix_todos_completed'), 'todos', ['completed'], unique=False)


def downgrade() -> None:
    """Drop initial tables."""
    op.drop_index(op.f('ix_todos_completed'), table_name='todos')
    op.drop_index(op.f('ix_todos_user_id'), table_name='todos')
    op.drop_index(op.f('ix_todos_id'), table_name='todos')
    op.drop_table('todos')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

