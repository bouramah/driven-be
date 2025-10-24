from app.common.models import PermissionPage, db
from datetime import datetime

class PermissionPageService:
    def get_all_permission_pages(self):
        return PermissionPage.query.all()
    
    def get_permission_page_by_id(self, pp_id):
        return PermissionPage.query.get(pp_id)
    
    def get_permission_pages_by_page(self, page_id):
        return PermissionPage.query.filter_by(page_id=page_id).all()
    
    def get_permission_pages_by_permission(self, permission_id):
        return PermissionPage.query.filter_by(permission_id=permission_id).all()
    
    def create_permission_page(self, pp_data):
        permission_page = PermissionPage(**pp_data)
        db.session.add(permission_page)
        db.session.commit()
        return permission_page
    
    def update_permission_page(self, pp_id, pp_data):
        permission_page = self.get_permission_page_by_id(pp_id)
        if not permission_page:
            return None
            
        for key, value in pp_data.items():
            setattr(permission_page, key, value)
            
        db.session.commit()
        return permission_page
    
    def delete_permission_page(self, pp_id):
        permission_page = self.get_permission_page_by_id(pp_id)
        if permission_page:
            db.session.delete(permission_page)
            db.session.commit()
            return True
        return False 