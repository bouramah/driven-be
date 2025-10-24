from app.common.services.objectif_service import ObjectifService

class ObjectifController:
    def __init__(self):
        self.objectif_service = ObjectifService()
    
    def get_all_objectifs(self):
        return self.objectif_service.get_all_objectifs()
    
    def get_all_objectifs_paginated(self, page, per_page):
        return self.objectif_service.get_all_objectifs_paginated(page, per_page)
    
    def get_objectif_by_id(self, objectif_id):
        return self.objectif_service.get_objectif_by_id(objectif_id)
    
    def get_objectifs_by_utilisateur(self, utilisateur_id):
        return self.objectif_service.get_objectifs_by_utilisateur(utilisateur_id)
    
    def get_objectifs_by_utilisateur_paginated(self, utilisateur_id, page, per_page):
        return self.objectif_service.get_objectifs_by_utilisateur_paginated(utilisateur_id, page, per_page)
    
    def create_objectif(self, objectif_data):
        return self.objectif_service.create_objectif(objectif_data)
    
    def update_objectif(self, objectif_id, objectif_data):
        return self.objectif_service.update_objectif(objectif_id, objectif_data)
    
    def delete_objectif(self, objectif_id):
        return self.objectif_service.delete_objectif(objectif_id)
    
    def get_objectifs_by_type(self, type_objectif):
        return self.objectif_service.get_objectifs_by_type(type_objectif)
    
    def get_objectifs_by_type_paginated(self, type_objectif, page, per_page):
        return self.objectif_service.get_objectifs_by_type_paginated(type_objectif, page, per_page)
    
    def get_objectifs_by_periode(self, periode):
        return self.objectif_service.get_objectifs_by_periode(periode)
    
    def get_objectifs_by_periode_paginated(self, periode, page, per_page):
        return self.objectif_service.get_objectifs_by_periode_paginated(periode, page, per_page) 