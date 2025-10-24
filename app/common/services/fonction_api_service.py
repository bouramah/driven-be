from app import db
from app.common.models import FonctionAPI, FonctionPermission, Permission
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

class FonctionAPIService:    
    def get_fonctions_paginated(self, page, per_page):
        """Lister toutes les fonctions API avec pagination"""
        return FonctionAPI.query.options(
            joinedload(FonctionAPI.application)
        ).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_fonctions_by_app_paginated(self, app_id, page, per_page):
        """Récupérer les fonctions API d'une application avec pagination"""
        return FonctionAPI.query.filter_by(app_id=app_id).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_fonction_by_id(self, fonction_id):
        """Récupérer une fonction API par son ID"""
        return FonctionAPI.query.options(
            joinedload(FonctionAPI.application)
        ).get(fonction_id)
    
    def get_fonctions_by_app(self, app_id):
        """Récupérer toutes les fonctions API d'une application"""
        return FonctionAPI.query.filter_by(app_id=app_id).all()
    
    def create_fonction(self, fonction_data):
        """Créer une nouvelle fonction API"""
        try:
            # Vérifier si une fonction avec le même nom existe déjà pour cette application
            existing_fonction = FonctionAPI.query.filter(
                and_(
                    FonctionAPI.nom_fonction == fonction_data.get('nom_fonction'),
                    FonctionAPI.app_id == fonction_data.get('app_id')
                )
            ).first()
            
            if existing_fonction:
                raise ValueError(f"Une fonction avec le nom '{fonction_data.get('nom_fonction')}' existe déjà pour cette application")
            
            # Créer la nouvelle fonction API
            nouvelle_fonction = FonctionAPI(
                nom_fonction=fonction_data.get('nom_fonction'),
                description=fonction_data.get('description'),
                app_id=fonction_data.get('app_id'),
                creer_par=fonction_data.get('creer_par'),
                modifier_par=fonction_data.get('modifier_par')
            )
            
            db.session.add(nouvelle_fonction)
            db.session.commit()
            return nouvelle_fonction
            
        except Exception as e:
            db.session.rollback()
            raise
    
    def update_fonction(self, fonction_id, fonction_data):
        """Mettre à jour une fonction API existante"""
        try:
            fonction = self.get_fonction_by_id(fonction_id)
            if not fonction:
                return None
            
            # Si le nom ou l'app_id change, vérifier l'unicité
            if ('nom_fonction' in fonction_data and fonction_data['nom_fonction'] != fonction.nom_fonction) or \
               ('app_id' in fonction_data and fonction_data['app_id'] != fonction.app_id):
                
                existing_fonction = FonctionAPI.query.filter(
                    and_(
                        FonctionAPI.nom_fonction == fonction_data.get('nom_fonction', fonction.nom_fonction),
                        FonctionAPI.app_id == fonction_data.get('app_id', fonction.app_id),
                        FonctionAPI.fonction_id != fonction_id
                    )
                ).first()
                
                if existing_fonction:
                    raise ValueError(f"Une fonction avec le nom '{fonction_data.get('nom_fonction')}' existe déjà pour cette application")
            
            # Mettre à jour les champs
            for key, value in fonction_data.items():
                setattr(fonction, key, value)
            
            db.session.commit()
            return fonction
            
        except Exception as e:
            db.session.rollback()
            raise
    
    def delete_fonction(self, fonction_id):
        """Supprimer une fonction API"""
        try:
            # Récupérer la fonction API
            fonction = self.get_fonction_by_id(fonction_id)
            if not fonction:
                return None
            
            # Supprimer la fonction API (les permissions associées seront supprimées en cascade)
            db.session.delete(fonction)
            db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"Error deleting fonction API: {str(e)}")
            db.session.rollback()
            raise
    
    def get_fonction_permissions(self, fonction_id):
        """Récupérer toutes les permissions associées à une fonction API"""
        try:
            # Récupérer la fonction API
            fonction = self.get_fonction_by_id(fonction_id)
            if not fonction:
                return None
            
            # Récupérer les permissions associées
            fonction_permissions = FonctionPermission.query.filter_by(fonction_id=fonction_id).all()
            permission_ids = [fp.permission_id for fp in fonction_permissions]
            permissions = Permission.query.filter(Permission.permission_id.in_(permission_ids)).all()
            
            return permissions
            
        except Exception as e:
            print(f"Error getting fonction permissions: {str(e)}")
            raise
    
    def assign_permissions(self, fonction_id, permission_ids):
        """Assigner des permissions à une fonction API"""
        try:
            # Récupérer la fonction API
            fonction = self.get_fonction_by_id(fonction_id)
            if not fonction:
                return None
            
            # Récupérer les permissions existantes pour éviter les doublons
            existing_permissions = FonctionPermission.query.filter_by(fonction_id=fonction_id).all()
            existing_permission_ids = [fp.permission_id for fp in existing_permissions]
            
            # Ajouter uniquement les nouvelles permissions
            for permission_id in permission_ids:
                if permission_id not in existing_permission_ids:
                    # Créer une nouvelle association
                    fonction_permission = FonctionPermission(
                        fonction_id=fonction_id,
                        permission_id=permission_id,
                        creer_par=fonction.modifier_par,  # Utiliser le même utilisateur
                        modifier_par=fonction.modifier_par
                    )
                    db.session.add(fonction_permission)
            
            db.session.commit()
            return fonction
            
        except Exception as e:
            print(f"Error assigning permissions: {str(e)}")
            db.session.rollback()
            raise
    
    def remove_permissions(self, fonction_id, permission_ids):
        """Retirer des permissions d'une fonction API"""
        try:
            # Récupérer la fonction API
            fonction = self.get_fonction_by_id(fonction_id)
            if not fonction:
                return None
            
            # Supprimer les associations spécifiées
            FonctionPermission.query.filter(
                and_(
                    FonctionPermission.fonction_id == fonction_id,
                    FonctionPermission.permission_id.in_(permission_ids)
                )
            ).delete(synchronize_session=False)
            
            db.session.commit()
            return fonction
            
        except Exception as e:
            print(f"Error removing permissions: {str(e)}")
            db.session.rollback()
            raise 