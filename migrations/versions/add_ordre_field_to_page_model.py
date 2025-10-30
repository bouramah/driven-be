"""Add ordre field to Page model

Revision ID: add_ordre_page
Revises: 5aa28b1bc4b4
Create Date: 2025-03-06 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = 'add_ordre_page'
down_revision = '5aa28b1bc4b4'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    """Vérifie si une colonne existe dans une table"""
    inspector = reflection.Inspector.from_engine(op.get_bind())
    if inspector.has_table(table_name):
        columns = [c['name'] for c in inspector.get_columns(table_name)]
        return column_name in columns
    return False


def upgrade():
    # Ajouter la colonne ordre à la table page si elle n'existe pas déjà
    if not column_exists('page', 'ordre'):
        with op.batch_alter_table('page', schema=None) as batch_op:
            batch_op.add_column(sa.Column('ordre', sa.Integer(), nullable=True))


def downgrade():
    # Retirer la colonne ordre de la table page
    if column_exists('page', 'ordre'):
        with op.batch_alter_table('page', schema=None) as batch_op:
            batch_op.drop_column('ordre')

