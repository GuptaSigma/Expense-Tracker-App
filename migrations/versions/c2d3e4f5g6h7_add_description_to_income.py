"""add description to income

Revision ID: c2d3e4f5g6h7
Revises: a1b2c3d4e5f6
Create Date: 2026-03-01 10:00:00.000000

Adds description column to the income table to support optional income descriptions.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'c2d3e4f5g6h7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def _column_exists(table_name, column_name):
    """Return True if *column_name* already exists in *table_name*."""
    bind = op.get_bind()
    insp = inspect(bind)
    columns = [col['name'] for col in insp.get_columns(table_name)]
    return column_name in columns


def upgrade():
    # Add description column to income table if it doesn't exist
    if not _column_exists('income', 'description'):
        op.add_column(
            'income',
            sa.Column('description', sa.String(length=500), nullable=True),
        )


def downgrade():
    # Remove description column from income table
    if _column_exists('income', 'description'):
        op.drop_column('income', 'description')
