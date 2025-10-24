from app.common.services.permission_page_service import PermissionPageService

class PermissionPageController:
    def __init__(self):
        self.permission_page_service = PermissionPageService()
    
    def get_all_permission_pages(self):
        return self.permission_page_service.get_all_permission_pages()
    
    def get_permission_page_by_id(self, pp_id):
        return self.permission_page_service.get_permission_page_by_id(pp_id)
    
    def get_permission_pages_by_page(self, page_id):
        return self.permission_page_service.get_permission_pages_by_page(page_id)
    
    def get_permission_pages_by_permission(self, permission_id):
        return self.permission_page_service.get_permission_pages_by_permission(permission_id)
    
    def create_permission_page(self, pp_data):
        return self.permission_page_service.create_permission_page(pp_data)
    
    def update_permission_page(self, pp_id, pp_data):
        return self.permission_page_service.update_permission_page(pp_id, pp_data)
    
    def delete_permission_page(self, pp_id):
        return self.permission_page_service.delete_permission_page(pp_id) 