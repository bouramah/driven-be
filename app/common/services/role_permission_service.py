from app.common.models import RolePermission, db
from datetime import datetime

class RolePermissionService:
    def get_all_role_permissions(self):
        return RolePermission.query.all()
    
    def get_role_permission_by_id(self, rp_id):
        return RolePermission.query.get(rp_id)
    
    def get_role_permissions_by_role(self, role_id):
        return RolePermission.query.filter_by(role_id=role_id).all()
    
    def get_role_permissions_by_permission_page(self, pp_id):
        return RolePermission.query.filter_by(pp_id=pp_id).all()
    
    def create_role_permission(self, rp_data):
        role_permission = RolePermission(**rp_data)
        db.session.add(role_permission)
        db.session.commit()
        return role_permission
    
    def update_role_permission(self, rp_id, rp_data):
        role_permission = self.get_role_permission_by_id(rp_id)
        if not role_permission:
            return None
            
        for key, value in rp_data.items():
            setattr(role_permission, key, value)
            
        db.session.commit()
        return role_permission
    
    def delete_role_permission(self, rp_id):
        role_permission = self.get_role_permission_by_id(rp_id)
        if role_permission:
            db.session.delete(role_permission)
            db.session.commit()
            return True
        return False
    
    def assign_permissions_to_role(self, role_id, permission_page_ids, user_id):
        for pp_id in permission_page_ids:
            role_permission = RolePermission(
                role_id=role_id,
                pp_id=pp_id,
                creer_par=user_id,
                modifier_par=user_id
            )
            db.session.add(role_permission)
        db.session.commit()
        return True
    
    def remove_permissions_from_role(self, role_id, permission_page_ids):
        RolePermission.query.filter(
            RolePermission.role_id == role_id,
            RolePermission.pp_id.in_(permission_page_ids)
        ).delete(synchronize_session=False)
        db.session.commit()
        return True 