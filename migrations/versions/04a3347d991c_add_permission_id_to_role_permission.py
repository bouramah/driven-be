"""add_permission_id_to_role_permission

Revision ID: 04a3347d991c
Revises: eb730c1339ee
Create Date: 2025-03-03 15:45:03.288089

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = '04a3347d991c'
down_revision = 'eb730c1339ee'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    """Vérifie si une colonne existe dans une table"""
    inspector = reflection.Inspector.from_engine(op.get_bind())
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    # Cette migration est maintenant gérée par la migration précédente
    pass


def downgrade():
    # Cette migration est maintenant gérée par la migration précédente
    pass
