"""Ajout des tables pour le contrôle d'accès aux endpoints

Revision ID: eb730c1339ee
Revises: a302f577ae72
Create Date: 2025-03-03 15:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = 'eb730c1339ee'
down_revision = 'a302f577ae72'
branch_labels = None
depends_on = None


def table_exists(table_name):
    """Vérifie si une table existe dans la base de données"""
    inspector = reflection.Inspector.from_engine(op.get_bind())
    return table_name in inspector.get_table_names()


def column_exists(table_name, column_name):
    """Vérifie si une colonne existe dans une table"""
    inspector = reflection.Inspector.from_engine(op.get_bind())
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade():
    # Création de la table endpoint si elle n'existe pas
    if not table_exists('endpoint'):
        op.create_table('endpoint',
            sa.Column('endpoint_id', sa.Integer(), nullable=False),
            sa.Column('url_pattern', sa.String(length=300), nullable=False),
            sa.Column('methode', sa.String(length=10), nullable=False),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('app_id', sa.Integer(), nullable=False),
            sa.Column('creer_par', sa.Integer(), nullable=False),
            sa.Column('modifier_par', sa.Integer(), nullable=False),
            sa.Column('creer_a', sa.DateTime(), nullable=False),
            sa.Column('modifier_a', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['app_id'], ['application.app_id'], name='fk_endpoint_app_id'),
            sa.PrimaryKeyConstraint('endpoint_id')
        )
    
    # Création de la table endpoint_permission si elle n'existe pas
    if not table_exists('endpoint_permission'):
        op.create_table('endpoint_permission',
            sa.Column('ep_id', sa.Integer(), nullable=False),
            sa.Column('endpoint_id', sa.Integer(), nullable=False),
            sa.Column('permission_id', sa.Integer(), nullable=False),
            sa.Column('creer_par', sa.Integer(), nullable=False),
            sa.Column('modifier_par', sa.Integer(), nullable=False),
            sa.Column('creer_a', sa.DateTime(), nullable=False),
            sa.Column('modifier_a', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['endpoint_id'], ['endpoint.endpoint_id'], name='fk_endpoint_permission_endpoint_id'),
            sa.ForeignKeyConstraint(['permission_id'], ['permission.permission_id'], name='fk_endpoint_permission_permission_id'),
            sa.PrimaryKeyConstraint('ep_id')
        )
    
    # Vérifier si la table role_permission existe
    if table_exists('role_permission'):
        # Vérifier si la colonne permission_id n'existe pas encore
        if not column_exists('role_permission', 'permission_id'):
            # Utiliser le mode batch pour SQLite
            with op.batch_alter_table('role_permission') as batch_op:
                # Ajouter la colonne permission_id
                batch_op.add_column(sa.Column('permission_id', sa.Integer(), nullable=True))
            
            # Mettre à jour les données existantes
            op.execute(text("UPDATE role_permission SET permission_id = pp_id"))
            
            # Rendre la colonne non nullable et ajouter la contrainte
            with op.batch_alter_table('role_permission') as batch_op:
                batch_op.alter_column('permission_id', nullable=False)
                batch_op.create_foreign_key(
                    'fk_role_permission_permission_id', 
                    'permission', 
                    ['permission_id'], ['permission_id']
                )
    else:
        # Création de la table role_permission si elle n'existe pas
        op.create_table('role_permission',
            sa.Column('rp_id', sa.Integer(), nullable=False),
            sa.Column('role_id', sa.Integer(), nullable=False),
            sa.Column('permission_id', sa.Integer(), nullable=False),
            sa.Column('pp_id', sa.Integer(), nullable=True),  # Pour compatibilité
            sa.Column('creer_par', sa.Integer(), nullable=False),
            sa.Column('modifier_par', sa.Integer(), nullable=False),
            sa.Column('creer_a', sa.DateTime(), nullable=False),
            sa.Column('modifier_a', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['permission_id'], ['permission.permission_id'], name='fk_role_permission_permission_id'),
            sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], name='fk_role_permission_role_id'),
            sa.PrimaryKeyConstraint('rp_id')
        )


def downgrade():
    # Suppression des tables si elles existent
    if table_exists('endpoint_permission'):
        op.drop_table('endpoint_permission')
    
    if table_exists('endpoint'):
        op.drop_table('endpoint')
    
    # Pour role_permission, on ne fait rien car c'est géré par la migration suivante 