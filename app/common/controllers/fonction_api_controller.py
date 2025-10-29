from app.common.services.fonction_api_service import FonctionAPIService

class FonctionAPIController:
    def __init__(self):
        self.fonction_api_service = FonctionAPIService()
    
    def get_fonctions_paginated(self, page, per_page):
        """Récupérer toutes les fonctions API avec pagination"""
        return self.fonction_api_service.get_fonctions_paginated(page, per_page)
    
    def get_fonctions_by_app_paginated(self, app_id, page, per_page):
        """Récupérer les fonctions API d'une application avec pagination"""
        return self.fonction_api_service.get_fonctions_by_app_paginated(app_id, page, per_page)
    
    def get_fonction_by_id(self, fonction_id):
        """Récupérer une fonction API par son ID"""
        return self.fonction_api_service.get_fonction_by_id(fonction_id)
    
    def get_fonctions_by_app(self, app_id):
        """Récupérer toutes les fonctions API d'une application"""
        return self.fonction_api_service.get_fonctions_by_app(app_id)
    
    def search_fonctions_paginated(self, search_term, page, per_page):
        """Rechercher des fonctions API avec pagination"""
        return self.fonction_api_service.search_fonctions_paginated(search_term, page, per_page)
    
    def create_fonction(self, fonction_data):
        """Créer une nouvelle fonction API"""
        return self.fonction_api_service.create_fonction(fonction_data)
    
    def update_fonction(self, fonction_id, fonction_data):
        """Mettre à jour une fonction API existante"""
        return self.fonction_api_service.update_fonction(fonction_id, fonction_data)
    
    def delete_fonction(self, fonction_id):
        """Supprimer une fonction API"""
        return self.fonction_api_service.delete_fonction(fonction_id)
    
    def get_fonction_permissions(self, fonction_id):
        """Récupérer toutes les permissions associées à une fonction API"""
        return self.fonction_api_service.get_fonction_permissions(fonction_id)
    
    def assign_permissions(self, fonction_id, permission_ids):
        """Assigner des permissions à une fonction API"""
        return self.fonction_api_service.assign_permissions(fonction_id, permission_ids)
    
    def remove_permissions(self, fonction_id, permission_ids):
        """Retirer des permissions d'une fonction API"""
        return self.fonction_api_service.remove_permissions(fonction_id, permission_ids) 