from app.common.services.application_service import ApplicationService

class ApplicationController:
    def __init__(self):
        self.application_service = ApplicationService()
    
    def get_all_applications(self):
        return self.application_service.get_all_applications()
    
    def get_application_by_id(self, app_id):
        return self.application_service.get_application_by_id(app_id)
    
    def create_application(self, app_data, icon_file=None):
        return self.application_service.create_application(app_data, icon_file)
    
    def update_application(self, app_id, app_data, icon_file=None):
        return self.application_service.update_application(app_id, app_data, icon_file)
    
    def delete_application(self, app_id):
        return self.application_service.delete_application(app_id) 