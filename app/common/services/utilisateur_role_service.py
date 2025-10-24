from app.common.models import UtilisateurRole, db

class UtilisateurRoleService:
    def get_user_roles(self, user_id):
        """Récupérer tous les rôles d'un utilisateur"""
        return UtilisateurRole.query.filter_by(id_utilisateur=user_id).all()
    
    def get_user_roles_by_app(self, user_id, app_id):
        """Récupérer les rôles d'un utilisateur pour une application spécifique"""
        return UtilisateurRole.query.filter_by(
            id_utilisateur=user_id,
            app_id=app_id
        ).all()
    
    def get_user_roles_paginated(self, user_id, page, per_page):
        """Récupérer les rôles d'un utilisateur avec pagination"""
        return UtilisateurRole.query.filter_by(
            id_utilisateur=user_id
        ).paginate(page=page, per_page=per_page, error_out=False)
    
    def assign_role(self, user_id, role_id, app_id, created_by):
        """Assigner un rôle à un utilisateur pour une application"""
        try:
            # Vérifier si l'association existe déjà
            existing = UtilisateurRole.query.filter_by(
                id_utilisateur=user_id,
                role_id=role_id,
                app_id=app_id
            ).first()
            
            if existing:
                return None
            
            user_role = UtilisateurRole(
                id_utilisateur=user_id,
                role_id=role_id,
                app_id=app_id,
                creer_par=created_by,
                modifier_par=created_by
            )
            
            db.session.add(user_role)
            db.session.commit()
            return user_role
            
        except Exception as e:
            print(f"Error assigning role: {str(e)}")
            db.session.rollback()
            raise
    
    def remove_role(self, user_id, role_id, app_id):
        """Retirer un rôle d'un utilisateur pour une application"""
        try:
            user_role = UtilisateurRole.query.filter_by(
                id_utilisateur=user_id,
                role_id=role_id,
                app_id=app_id
            ).first()
            
            if user_role:
                db.session.delete(user_role)
                db.session.commit()
                return True
            return False
            
        except Exception as e:
            print(f"Error removing role: {str(e)}")
            db.session.rollback()
            raise
    
    def remove_all_roles(self, user_id, app_id):
        """Retirer tous les rôles d'un utilisateur pour une application"""
        try:
            UtilisateurRole.query.filter_by(
                id_utilisateur=user_id,
                app_id=app_id
            ).delete()
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error removing all roles: {str(e)}")
            db.session.rollback()
            raise 