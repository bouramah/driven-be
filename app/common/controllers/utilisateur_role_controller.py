from app.common.services.utilisateur_role_service import UtilisateurRoleService

class UtilisateurRoleController:
    def __init__(self):
        self.utilisateur_role_service = UtilisateurRoleService()
    
    def get_user_roles(self, user_id):
        return self.utilisateur_role_service.get_user_roles(user_id)
    
    def get_user_roles_by_app(self, user_id, app_id):
        return self.utilisateur_role_service.get_user_roles_by_app(user_id, app_id)
    
    def get_user_roles_paginated(self, user_id, page, per_page):
        return self.utilisateur_role_service.get_user_roles_paginated(user_id, page, per_page)
    
    def assign_role(self, user_id, role_id, app_id, created_by):
        return self.utilisateur_role_service.assign_role(user_id, role_id, app_id, created_by)
    
    def remove_role(self, user_id, role_id, app_id):
        return self.utilisateur_role_service.remove_role(user_id, role_id, app_id)
    
    def remove_all_roles(self, user_id, app_id):
        return self.utilisateur_role_service.remove_all_roles(user_id, app_id) 