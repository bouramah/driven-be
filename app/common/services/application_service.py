from app.common.models import Application, Utilisateur, UtilisateurRole, db
from app.common.utils.file_manager import FileManager
from sqlalchemy.orm import joinedload

class ApplicationService:
    def __init__(self):
        self.file_manager = FileManager(
            upload_folder='uploads/icons',
            allowed_extensions={'png', 'jpg', 'jpeg', 'gif', 'svg'}
        )

    def get_all_applications(self):
        return Application.query.all()
    
    def get_application_by_id(self, app_id):
        return Application.query.get(app_id)
    
    def get_applications_for_user(self, user: Utilisateur):
        """Retourner les applications accessibles à l'utilisateur.
        - Si le profil de l'utilisateur est 'Administrateur', retourner toutes les applications
        - Sinon, retourner uniquement les applications pour lesquelles il a au moins un rôle
        """
        if not user:
            return []

        # Accès complet pour les administrateurs
        if getattr(user, 'profile', None) == 'Administrateur' or getattr(user, 'profil', None) == 'Administrateur':
            return Application.query.all()

        # Récupérer les app_id distincts où l'utilisateur possède au moins un rôle
        app_ids = db.session.query(UtilisateurRole.app_id).filter_by(id_utilisateur=user.id_utilisateur).distinct().all()
        app_ids = [row[0] for row in app_ids]

        if not app_ids:
            return []

        # Retourner les applications correspondantes
        return Application.query.filter(Application.app_id.in_(app_ids)).all()
    
    def get_utilisateurs_by_application_paginated(self, app_id, page, per_page):
        """Récupérer tous les utilisateurs d'une application avec pagination"""
        # Récupérer les IDs des utilisateurs ayant un rôle pour cette application
        user_ids = db.session.query(UtilisateurRole.id_utilisateur).filter_by(app_id=app_id).distinct().all()
        user_ids = [id[0] for id in user_ids]  # Convertir les tuples en liste simple
        
        if not user_ids:
            # Retourner une pagination vide si aucun utilisateur
            # Utiliser une condition impossible pour créer une pagination vide
            return Utilisateur.query.filter(Utilisateur.id_utilisateur < 0).paginate(
                page=page, per_page=per_page, error_out=False
            )
        
        # Récupérer les utilisateurs correspondants avec leurs relations
        return Utilisateur.query.options(
            joinedload(Utilisateur.utilisateur_roles).joinedload(UtilisateurRole.application),
            joinedload(Utilisateur.entite)
        ).filter(Utilisateur.id_utilisateur.in_(user_ids)).paginate(page=page, per_page=per_page, error_out=False)
    
    def create_application(self, app_data, icon_file=None):
        # Vérifier si une application avec le même nom existe déjà
        existing_app = Application.query.filter_by(nom=app_data.get('nom')).first()
        if existing_app:
            raise ValueError(f"Une application avec le nom '{app_data.get('nom')}' existe déjà")

        if icon_file:
            icon_path = self.file_manager.save_file(icon_file)
            if icon_path:
                app_data['app_icon'] = icon_path

        application = Application(**app_data)
        db.session.add(application)
        db.session.commit()
        return application
    
    def update_application(self, app_id, app_data, icon_file=None):
        application = self.get_application_by_id(app_id)
        if not application:
            return None
            
        # Si le nom est modifié, vérifier qu'il n'existe pas déjà
        if 'nom' in app_data and app_data['nom'] != application.nom:
            existing_app = Application.query.filter_by(nom=app_data['nom']).first()
            if existing_app:
                raise ValueError(f"Une application avec le nom '{app_data['nom']}' existe déjà")
            
        if icon_file:
            # Supprimer l'ancienne icône si elle existe
            if application.app_icon:
                self.file_manager.delete_file(application.app_icon)
            
            # Sauvegarder la nouvelle icône
            icon_path = self.file_manager.save_file(icon_file)
            if icon_path:
                app_data['app_icon'] = icon_path
            
        for key, value in app_data.items():
            setattr(application, key, value)
            
        db.session.commit()
        return application
    
    def delete_application(self, app_id):
        application = self.get_application_by_id(app_id)
        if application:
            # Supprimer l'icône si elle existe
            if application.app_icon:
                self.file_manager.delete_file(application.app_icon)
                
            db.session.delete(application)
            db.session.commit()
            return True
        return False 