"""add missing user columns

Revision ID: a1b2c3d4e5f6
Revises: 82138cbcc4b5
Create Date: 2026-02-28 05:30:00.000000

Adds columns that were introduced after the initial db.create_all() baseline:
  - google_id         VARCHAR(500) UNIQUE nullable
  - is_email_verified BOOLEAN NOT NULL DEFAULT false
  - otp               VARCHAR(6) nullable
  - otp_expiry        TIMESTAMP nullable

Also alters `password` to be nullable (Google-OAuth users have no password hash).
Each column addition is guarded by a check so the migration is safe to run
against databases where the columns already exist (e.g. created by create_all).
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '82138cbcc4b5'
branch_labels = None
depends_on = None


def _column_exists(table_name, column_name):
    """Return True if *column_name* already exists in *table_name*."""
    bind = op.get_bind()
    insp = inspect(bind)
    columns = [col['name'] for col in insp.get_columns(table_name)]
    return column_name in columns


def upgrade():
    # --- google_id -----------------------------------------------------------
    if not _column_exists('user', 'google_id'):
        op.add_column(
            'user',
            sa.Column('google_id', sa.String(length=500), nullable=True),
        )
        op.create_unique_constraint('uq_user_google_id', 'user', ['google_id'])

    # --- is_email_verified ---------------------------------------------------
    if not _column_exists('user', 'is_email_verified'):
        op.add_column(
            'user',
            sa.Column(
                'is_email_verified',
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )

    # --- otp -----------------------------------------------------------------
    if not _column_exists('user', 'otp'):
        op.add_column(
            'user',
            sa.Column('otp', sa.String(length=6), nullable=True),
        )

    # --- otp_expiry ----------------------------------------------------------
    if not _column_exists('user', 'otp_expiry'):
        op.add_column(
            'user',
            sa.Column('otp_expiry', sa.DateTime(), nullable=True),
        )

    # --- password: make nullable (Google OAuth users have no password) -------
    op.alter_column('user', 'password', existing_type=sa.String(length=200),
                    nullable=True)


def _constraint_exists(table_name, constraint_name):
    """Return True if *constraint_name* exists on *table_name*."""
    bind = op.get_bind()
    insp = inspect(bind)
    uqs = insp.get_unique_constraints(table_name)
    return any(uq['name'] == constraint_name for uq in uqs)


def downgrade():
    op.alter_column('user', 'password', existing_type=sa.String(length=200),
                    nullable=False)
    if _column_exists('user', 'otp_expiry'):
        op.drop_column('user', 'otp_expiry')
    if _column_exists('user', 'otp'):
        op.drop_column('user', 'otp')
    if _column_exists('user', 'is_email_verified'):
        op.drop_column('user', 'is_email_verified')
    if _constraint_exists('user', 'uq_user_google_id'):
        op.drop_constraint('uq_user_google_id', 'user', type_='unique')
    if _column_exists('user', 'google_id'):
        op.drop_column('user', 'google_id')
