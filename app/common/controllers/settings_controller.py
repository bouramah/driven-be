from app.common.services.settings_service import SettingsService

class SettingsController:
    def __init__(self):
        self.settings_service = SettingsService()
    
    def get_all_settings(self):
        return self.settings_service.get_all_settings()
    
    def get_all_settings_paginated(self, page, per_page):
        return self.settings_service.get_all_settings_paginated(page, per_page)
    
    def get_setting_by_id(self, setting_id):
        return self.settings_service.get_setting_by_id(setting_id)
    
    def get_settings_by_utilisateur(self, utilisateur_id):
        return self.settings_service.get_settings_by_utilisateur(utilisateur_id)
    
    def get_settings_by_utilisateur_paginated(self, utilisateur_id, page, per_page):
        return self.settings_service.get_settings_by_utilisateur_paginated(utilisateur_id, page, per_page)
    
    def get_setting_by_key(self, key):
        return self.settings_service.get_setting_by_key(key)
    
    def create_setting(self, setting_data):
        return self.settings_service.create_setting(setting_data)
    
    def update_setting(self, setting_id, setting_data):
        return self.settings_service.update_setting(setting_id, setting_data)
    
    def delete_setting(self, setting_id):
        return self.settings_service.delete_setting(setting_id) 