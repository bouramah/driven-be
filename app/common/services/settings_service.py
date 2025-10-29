from app.common.models import Settings, Codification, db
from sqlalchemy.orm import joinedload

class SettingsService:
    def get_all_settings(self):
        return Settings.query.options(joinedload(Settings.codification)).all()
    
    def get_all_settings_paginated(self, page, per_page):
        pagination = Settings.query.options(
            joinedload(Settings.codification)
        ).paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total
    
    def get_setting_by_id(self, setting_id):
        return Settings.query.options(
            joinedload(Settings.codification)
        ).get(setting_id)
    
    def get_settings_by_utilisateur(self, utilisateur_id):
        return Settings.query.options(
            joinedload(Settings.codification)
        ).filter_by(id_utilisateur=utilisateur_id).all()
    
    def get_settings_by_utilisateur_paginated(self, utilisateur_id, page, per_page):
        pagination = Settings.query.options(
            joinedload(Settings.codification)
        ).filter_by(id_utilisateur=utilisateur_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return pagination.items, pagination.pages, pagination.total
    
    def get_setting_by_user_and_codification(self, utilisateur_id, codification_id):
        return Settings.query.filter_by(
            id_utilisateur=utilisateur_id,
            id_codification=codification_id
        ).first()
    
    def create_setting(self, setting_data):
        # Vérifier qu'il n'existe pas déjà un setting pour ce param et cet utilisateur
        existing_setting = Settings.query.filter_by(
            id_utilisateur=setting_data['id_utilisateur'],
            id_codification=setting_data['id_codification']
        ).first()
        
        if existing_setting:
            raise ValueError("Un paramètre avec cette codification existe déjà pour cet utilisateur")

        setting = Settings(**setting_data)
        db.session.add(setting)
        db.session.commit()
        return self.get_setting_by_id(setting.id_set)  # Retourner avec la codification chargée
    
    def update_setting(self, setting_id, setting_data):
        setting = self.get_setting_by_id(setting_id)
        if not setting:
            return None
            
        # Si on change la codification, vérifier qu'il n'existe pas déjà
        if 'id_codification' in setting_data and setting_data['id_codification'] != setting.id_codification:
            existing_setting = Settings.query.filter_by(
                id_utilisateur=setting.id_utilisateur,
                id_codification=setting_data['id_codification']
            ).first()
            if existing_setting:
                raise ValueError("Un paramètre avec cette codification existe déjà pour cet utilisateur")
            
        for key, value in setting_data.items():
            setattr(setting, key, value)
            
        db.session.commit()
        return self.get_setting_by_id(setting_id)  # Retourner avec la codification chargée
    
    def delete_setting(self, setting_id):
        setting = self.get_setting_by_id(setting_id)
        if setting:
            db.session.delete(setting)
            db.session.commit()
            return True
        return False 