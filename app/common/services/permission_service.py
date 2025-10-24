from app.common.models import Permission, db, RolePermission, Role

class PermissionService:    
    def get_permissions_paginated(self, page, per_page):
        """Lister toutes les permissions avec pagination"""
        return Permission.query.paginate(page=page, per_page=per_page, error_out=False)
    
    def get_permission_by_id(self, permission_id):
        return Permission.query.get(permission_id)
    
    def create_permission(self, permission_data):
        try:
            # Convertir 'name' en 'nom' si nécessaire
            if 'name' in permission_data:
                permission_data['nom'] = permission_data.pop('name')
            
            # Vérifier si une permission avec le même nom existe déjà
            existing_permission = Permission.query.filter_by(nom=permission_data['nom']).first()
            if existing_permission:
                raise ValueError(f"Une permission avec le nom '{permission_data['nom']}' existe déjà")
            
            # Créer la permission avec les données fournies
            permission = Permission(**permission_data)
            db.session.add(permission)
            db.session.commit()
            return permission
        except Exception as e:
            print(f"Error creating permission: {str(e)}")
            db.session.rollback()
            raise
    
    def update_permission(self, permission_id, permission_data):
        try:
            permission = self.get_permission_by_id(permission_id)
            if not permission:
                return None
            
            # Si le nom est modifié, vérifier qu'il n'existe pas déjà
            if 'nom' in permission_data and permission_data['nom'] != permission.nom:
                existing_permission = Permission.query.filter(
                    Permission.nom == permission_data['nom'],
                    Permission.permission_id != permission_id
                ).first()
                if existing_permission:
                    raise ValueError(f"Une permission avec le nom '{permission_data['nom']}' existe déjà")
                
            for key, value in permission_data.items():
                setattr(permission, key, value)
                
            db.session.commit()
            return permission
        except Exception as e:
            print(f"Error updating permission: {str(e)}")
            db.session.rollback()
            raise
    
    def delete_permission(self, permission_id):
        permission = self.get_permission_by_id(permission_id)
        if permission:
            db.session.delete(permission)
            db.session.commit()
            return True
        return False
    
    def get_roles_with_permission(self, permission_id):
        """Obtenir les rôles qui ont une permission spécifique"""
        try:
            permission = self.get_permission_by_id(permission_id)
            if not permission:
                return []
            
            # Récupérer les IDs des rôles associés à cette permission
            role_ids = [rp.role_id for rp in RolePermission.query.filter_by(permission_id=permission_id).all()]
            
            # Récupérer les objets Role correspondants
            roles = Role.query.filter(Role.role_id.in_(role_ids)).all()
            
            return roles
        except Exception as e:
            print(f"Error getting roles with permission: {str(e)}")
            raise