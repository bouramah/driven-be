from app.common.models import Application, db
from app.common.utils.file_manager import FileManager

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