from app.apps.gestion_demande.services.type_demande_service import TypeDemandeService

class TypeDemandeController:
    def __init__(self):
        self.type_demande_service = TypeDemandeService()
    
    def get_all_types_demande(self):
        return self.type_demande_service.get_all_types_demande()
    
    def get_type_demande_by_id(self, type_id):
        return self.type_demande_service.get_type_demande_by_id(type_id)
    
    def create_type_demande(self, type_data):
        return self.type_demande_service.create_type_demande(type_data)
    
    def update_type_demande(self, type_id, type_data):
        return self.type_demande_service.update_type_demande(type_id, type_data)
    
    def delete_type_demande(self, type_id):
        return self.type_demande_service.delete_type_demande(type_id) 