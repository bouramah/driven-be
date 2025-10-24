from app.common.services.entite_service import EntiteService

class EntiteController:
    def __init__(self):
        self.entite_service = EntiteService()
    
    def get_all_entites(self):
        return self.entite_service.get_all_entites()
    
    def get_entites_paginated(self, page, per_page):
        return self.entite_service.get_entites_paginated(page, per_page)
    
    def get_entite_by_id(self, entite_id):
        return self.entite_service.get_entite_by_id(entite_id)
    
    def get_entite_by_code(self, code):
        return self.entite_service.get_entite_by_code(code)
    
    def create_entite(self, entite_data):
        return self.entite_service.create_entite(entite_data)
    
    def update_entite(self, entite_id, entite_data):
        return self.entite_service.update_entite(entite_id, entite_data)
    
    def delete_entite(self, entite_id):
        return self.entite_service.delete_entite(entite_id) 