"""add_value_configuration_to_codification

Revision ID: 5abd8d451860
Revises: a966f889d7d1
Create Date: 2025-10-28 19:29:58.878966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5abd8d451860'
down_revision = 'a966f889d7d1'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to codification table
    op.add_column('codification', sa.Column('type_valeur', sa.String(50), nullable=False, server_default='text'))
    op.add_column('codification', sa.Column('valeurs_possibles', sa.Text(), nullable=True))
    op.add_column('codification', sa.Column('valeur_defaut', sa.String(500), nullable=True))
    op.add_column('codification', sa.Column('obligatoire', sa.Boolean(), nullable=False, server_default='1'))


def downgrade():
    # Remove columns from codification table
    op.drop_column('codification', 'obligatoire')
    op.drop_column('codification', 'valeur_defaut')
    op.drop_column('codification', 'valeurs_possibles')
    op.drop_column('codification', 'type_valeur')
