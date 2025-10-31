from app.common.models import Role, Permission, RolePermission, Application, db
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload

class RoleService:    
    def get_roles_paginated(self, page, per_page):
        """Lister tous les rôles avec pagination et les informations de l'application"""
        return Role.query.options(
            joinedload(Role.application)
        ).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_roles_by_app_paginated(self, app_id, page, per_page):
        """Lister tous les rôles d'une application avec pagination"""
        return Role.query.filter_by(app_id=app_id).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_role_by_id(self, role_id):
        """Récupérer un rôle par son ID avec les informations de l'application"""
        return Role.query.options(
            joinedload(Role.application)
        ).get(role_id)
    
    def get_roles_by_app(self, app_id):
        """Récupérer tous les rôles d'une application"""
        return Role.query.filter_by(app_id=app_id).all()
    
    def create_role(self, role_data):
        """Créer un rôle"""
        try:
            # Vérifier que l'application existe
            if 'app_id' not in role_data:
                raise ValueError("L'ID de l'application est requis pour créer un rôle")
            
            app = Application.query.get(role_data['app_id'])
            if not app:
                raise ValueError(f"L'application avec l'ID {role_data['app_id']} n'existe pas")
            
            # Vérifier si un rôle avec le même nom existe déjà pour cette application
            existing_role = Role.query.filter(
                and_(
                    Role.nom == role_data['nom'],
                    Role.app_id == role_data['app_id']
                )
            ).first()
            
            if existing_role:
                raise ValueError(f"Un rôle avec le nom '{role_data['nom']}' existe déjà pour cette application")
            
            # Créer le rôle
            role = Role(**role_data)
            db.session.add(role)
            db.session.commit()
            return role
            
        except Exception as e:
            print(f"Error creating role: {str(e)}")
            db.session.rollback()
            raise
    
    def update_role(self, role_id, role_data):
        """Modifier un rôle"""
        try:
            role = self.get_role_by_id(role_id)
            if not role:
                return None
            
            # Si on change l'application, vérifier qu'elle existe
            if 'app_id' in role_data and role_data['app_id'] != role.app_id:
                app = Application.query.get(role_data['app_id'])
                if not app:
                    raise ValueError(f"L'application avec l'ID {role_data['app_id']} n'existe pas")
            
            # Si on change le nom, vérifier qu'il n'existe pas déjà pour cette application
            if 'nom' in role_data and role_data['nom'] != role.nom:
                existing_role = Role.query.filter(
                    and_(
                        Role.nom == role_data['nom'],
                        Role.app_id == role_data.get('app_id', role.app_id),
                        Role.role_id != role_id
                    )
                ).first()
                
                if existing_role:
                    raise ValueError(f"Un rôle avec le nom '{role_data['nom']}' existe déjà pour cette application")
            
            # Mettre à jour le rôle
            for key, value in role_data.items():
                setattr(role, key, value)
                
            db.session.commit()
            return role
            
        except Exception as e:
            print(f"Error updating role: {str(e)}")
            db.session.rollback()
            raise
    
    def delete_role(self, role_id):
        """Supprimer un rôle"""
        try:
            role = self.get_role_by_id(role_id)
            if not role:
                return False
            
            # Vérifier si des utilisateurs ont ce rôle
            if role.utilisateur_roles:
                return None  # Le rôle est utilisé par des utilisateurs
            
            # Supprimer toutes les permissions associées
            RolePermission.query.filter_by(role_id=role_id).delete()
            
            # Supprimer le rôle
            db.session.delete(role)
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error deleting role: {str(e)}")
            db.session.rollback()
            raise
    
    def get_role_permissions(self, role_id):
        """Afficher les permissions d'un rôle"""
        try:
            role = self.get_role_by_id(role_id)
            if not role:
                return []
            
            # Récupérer les IDs des permissions associées au rôle
            permission_ids = [rp.permission_id for rp in RolePermission.query.filter_by(role_id=role_id).all()]
            
            # Récupérer les objets Permission correspondants
            permissions = Permission.query.filter(Permission.permission_id.in_(permission_ids)).all()
            
            return permissions
            
        except Exception as e:
            print(f"Error getting role permissions: {str(e)}")
            raise
    
    def assign_permissions(self, role_id, permission_ids):
        """Affecter des permissions à un rôle"""
        try:
            role = self.get_role_by_id(role_id)
            if not role:
                return None
            
            # Récupérer les permissions existantes
            existing_permissions = set(rp.permission_id for rp in RolePermission.query.filter_by(role_id=role_id).all())
            
            # Ajouter uniquement les nouvelles permissions
            for permission_id in permission_ids:
                if permission_id not in existing_permissions:
                    role_permission = RolePermission(
                        role_id=role_id,
                        permission_id=permission_id,
                        creer_par=role.creer_par,
                        modifier_par=role.modifier_par
                    )
                    db.session.add(role_permission)
            
            db.session.commit()
            return role
            
        except Exception as e:
            print(f"Error assigning permissions: {str(e)}")
            db.session.rollback()
            raise
    
    def remove_permissions(self, role_id, permission_ids):
        """Retirer des permissions d'un rôle"""
        try:
            role = self.get_role_by_id(role_id)
            if not role:
                return None
            
            # Supprimer les associations spécifiées
            RolePermission.query.filter(
                and_(
                    RolePermission.role_id == role_id,
                    RolePermission.permission_id.in_(permission_ids)
                )
            ).delete(synchronize_session=False)
            
            db.session.commit()
            return role
            
        except Exception as e:
            print(f"Error removing permissions: {str(e)}")
            db.session.rollback()
            raise
    
    def search_roles(self, query, page, per_page):
        """Rechercher des rôles par nom, description ou nom d'application"""
        search_query = f"%{query}%"
        return Role.query.options(
            joinedload(Role.application)
        ).join(Application).filter(
            or_(
                Role.nom.ilike(search_query),
                Role.description.ilike(search_query),
                Application.nom.ilike(search_query)
            )
        ).paginate(page=page, per_page=per_page, error_out=False)