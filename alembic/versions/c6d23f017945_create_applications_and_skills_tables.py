"""create applications and skills tables

Revision ID: c6d23f017945
Revises: 
Create Date: 2026-10-30
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c6d23f017945'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, nullable=False, server_default='1'),
        sa.Column('company', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=False),
        sa.Column('location', sa.String, nullable=False),
        sa.Column('date_applied', sa.Date, nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('job_link', sa.String, nullable=True, server_default=''),
        sa.Column('notes', sa.Text, nullable=True, server_default=''),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('NOW()'), nullable=False),
        sa.CheckConstraint(
            "status IN ('Applied', 'Online Assessment', 'Interview', 'Offer', 'Rejected')",
            name='ck_applications_status'
        ),
    )

    op.create_index('ix_applications_user_id', 'applications', ['user_id'])
    op.create_index('ix_applications_user_id_status', 'applications', ['user_id', 'status'])

    op.create_table(
        'skills',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table('skills')
    op.drop_index('ix_applications_user_id_status', table_name='applications')
    op.drop_index('ix_applications_user_id', table_name='applications')
    op.drop_table('applications')
