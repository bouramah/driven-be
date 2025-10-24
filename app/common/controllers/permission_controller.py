from app.common.services.permission_service import PermissionService

class PermissionController:
    def __init__(self):
        self.permission_service = PermissionService()
    
    
    def get_permissions_paginated(self, page, per_page):
        return self.permission_service.get_permissions_paginated(page, per_page)
    
    def get_permission_by_id(self, permission_id):
        return self.permission_service.get_permission_by_id(permission_id)
    
    def create_permission(self, permission_data):
        return self.permission_service.create_permission(permission_data)
    
    def update_permission(self, permission_id, permission_data):
        return self.permission_service.update_permission(permission_id, permission_data)
    
    def delete_permission(self, permission_id):
        return self.permission_service.delete_permission(permission_id)
    
    def get_roles_with_permission(self, permission_id):
        return self.permission_service.get_roles_with_permission(permission_id) 