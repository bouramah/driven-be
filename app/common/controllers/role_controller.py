from app.common.services.role_service import RoleService
from sqlalchemy.orm import joinedload
from app.common.models import Role, RolePermission, Permission

class RoleController:
    def __init__(self):
        self.role_service = RoleService()
    
    def get_roles_paginated(self, page, per_page):
        """Lister tous les rôles avec pagination"""
        return Role.query.options(
            joinedload(Role.role_permissions).joinedload(RolePermission.permission)
        ).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_roles_by_app_paginated(self, app_id, page, per_page):
        """Lister tous les rôles d'une application avec pagination"""
        return self.role_service.get_roles_by_app_paginated(app_id, page, per_page)
    
    def get_role_by_id(self, role_id):
        """Afficher un rôle spécifique"""
        return Role.query.options(
            joinedload(Role.role_permissions).joinedload(RolePermission.permission)
        ).filter_by(role_id=role_id).first()
    
    def get_roles_by_app(self, app_id):
        """Récupérer tous les rôles d'une application"""
        return self.role_service.get_roles_by_app(app_id)
    
    def create_role(self, role_data):
        """Créer un rôle"""
        return self.role_service.create_role(role_data)
    
    def update_role(self, role_id, role_data):
        """Modifier un rôle"""
        return self.role_service.update_role(role_id, role_data)
    
    def delete_role(self, role_id):
        """Supprimer un rôle"""
        return self.role_service.delete_role(role_id)
    
    def get_role_permissions(self, role_id):
        """Afficher les permissions d'un rôle"""
        return self.role_service.get_role_permissions(role_id)
    
    def assign_permissions(self, role_id, permission_ids):
        """Affecter des permissions à un rôle"""
        return self.role_service.assign_permissions(role_id, permission_ids)
    
    def remove_permissions(self, role_id, permission_ids):
        """Retirer des permissions d'un rôle"""
        return self.role_service.remove_permissions(role_id, permission_ids)
    
    def search_roles(self, query, page, per_page):
        """Rechercher des rôles par nom, description ou nom d'application"""
        return self.role_service.search_roles(query, page, per_page)