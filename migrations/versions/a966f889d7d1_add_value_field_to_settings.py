"""add_value_field_to_settings

Revision ID: a966f889d7d1
Revises: 1deff5bad3e8
Create Date: 2025-10-28 19:18:50.155699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a966f889d7d1'
down_revision = '1deff5bad3e8'
branch_labels = None
depends_on = None


def upgrade():
    # Add the value column to settings table
    op.add_column('settings', sa.Column('value', sa.String(500), nullable=False, server_default=''))
    op.add_column('settings', sa.Column('creer_par', sa.Integer(), nullable=True))
    op.add_column('settings', sa.Column('modifier_par', sa.Integer(), nullable=True))
    op.add_column('settings', sa.Column('creer_a', sa.DateTime(), nullable=True))
    op.add_column('settings', sa.Column('modifier_a', sa.DateTime(), nullable=True))


def downgrade():
    # Remove the columns from settings table
    op.drop_column('settings', 'modifier_a')
    op.drop_column('settings', 'creer_a')
    op.drop_column('settings', 'modifier_par')
    op.drop_column('settings', 'creer_par')
    op.drop_column('settings', 'value')
