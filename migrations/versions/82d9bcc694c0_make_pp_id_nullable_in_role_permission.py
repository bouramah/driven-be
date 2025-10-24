"""make_pp_id_nullable_in_role_permission

Revision ID: 82d9bcc694c0
Revises: 04a3347d991c
Create Date: 2025-03-03 15:54:02.984464

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = '82d9bcc694c0'
down_revision = '04a3347d991c'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    """Vérifie si une colonne existe dans une table"""
    inspector = reflection.Inspector.from_engine(op.get_bind())
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    return column_name in columns


def get_foreign_keys(table_name):
    """Récupère les clés étrangères d'une table"""
    inspector = reflection.Inspector.from_engine(op.get_bind())
    return inspector.get_foreign_keys(table_name)


def upgrade():
    # Vérifier si les colonnes existent
    if column_exists('role_permission', 'pp_id') and column_exists('role_permission', 'permission_id'):
        # Mettre à jour permission_id avec les valeurs de pp_id pour les enregistrements où permission_id est NULL
        op.execute('UPDATE role_permission SET permission_id = pp_id WHERE permission_id IS NULL')
    
    # Utiliser batch_alter_table pour les modifications de schéma
    with op.batch_alter_table('role_permission', schema=None) as batch_op:
        # Rendre permission_id non nullable si la colonne existe
        if column_exists('role_permission', 'permission_id'):
            batch_op.alter_column('permission_id',
                   existing_type=sa.INTEGER(),
                   nullable=False)
        
        # Vérifier si pp_id existe avant de supprimer sa contrainte et la colonne
        if column_exists('role_permission', 'pp_id'):
            # Récupérer les clés étrangères pour vérifier si la contrainte existe
            fks = get_foreign_keys('role_permission')
            pp_id_fk = None
            for fk in fks:
                if 'pp_id' in fk['constrained_columns']:
                    pp_id_fk = fk['name']
                    break
            
            # Supprimer la contrainte si elle existe
            if pp_id_fk:
                batch_op.drop_constraint(pp_id_fk, type_='foreignkey')
            
            # Créer la contrainte sur permission_id si elle n'existe pas déjà
            permission_id_fk = None
            for fk in fks:
                if 'permission_id' in fk['constrained_columns']:
                    permission_id_fk = fk['name']
                    break
            
            if not permission_id_fk and column_exists('role_permission', 'permission_id'):
                batch_op.create_foreign_key('fk_role_permission_permission_id', 'permission', ['permission_id'], ['permission_id'])
            
            # Supprimer la colonne pp_id
            batch_op.drop_column('pp_id')


def downgrade():
    with op.batch_alter_table('role_permission', schema=None) as batch_op:
        # Ajouter la colonne pp_id
        batch_op.add_column(sa.Column('pp_id', sa.INTEGER(), nullable=True))
        
        # Mettre à jour les valeurs de pp_id à partir de permission_id
        op.execute('UPDATE role_permission SET pp_id = permission_id')
        
        # Rendre pp_id non nullable
        batch_op.alter_column('pp_id', nullable=False)
        
        # Récupérer les clés étrangères pour vérifier si la contrainte existe
        fks = get_foreign_keys('role_permission')
        permission_id_fk = None
        for fk in fks:
            if 'permission_id' in fk['constrained_columns']:
                permission_id_fk = fk['name']
                break
        
        # Supprimer la contrainte sur permission_id si elle existe
        if permission_id_fk:
            batch_op.drop_constraint(permission_id_fk, type_='foreignkey')
        
        # Créer la contrainte sur pp_id
        batch_op.create_foreign_key('fk_role_permission_pp_id', 'permission_page', ['pp_id'], ['pp_id'])
        
        # Rendre permission_id nullable
        batch_op.alter_column('permission_id',
               existing_type=sa.INTEGER(),
               nullable=True)
