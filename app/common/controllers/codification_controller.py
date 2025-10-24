from app.common.services.codification_service import CodificationService

class CodificationController:
    def __init__(self):
        self.codification_service = CodificationService()
    
    def get_all_codifications(self):
        return self.codification_service.get_all_codifications()
    
    def get_all_codifications_paginated(self, page, per_page):
        return self.codification_service.get_all_codifications_paginated(page, per_page)
    
    def get_codification_by_id(self, codification_id):
        return self.codification_service.get_codification_by_id(codification_id)
    
    def get_codification_by_param(self, param):
        return self.codification_service.get_codification_by_param(param)
    
    def create_codification(self, codification_data):
        return self.codification_service.create_codification(codification_data)
    
    def update_codification(self, codification_id, codification_data):
        return self.codification_service.update_codification(codification_id, codification_data)
    
    def delete_codification(self, codification_id):
        return self.codification_service.delete_codification(codification_id)
    
    def search_codifications(self, search_term):
        return self.codification_service.search_codifications(search_term)
    
    def search_codifications_paginated(self, search_term, page, per_page):
        return self.codification_service.search_codifications_paginated(search_term, page, per_page) 