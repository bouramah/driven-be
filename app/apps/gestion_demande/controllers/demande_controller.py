from app.apps.gestion_demande.services.demande_service import DemandeService

class DemandeController:
    def __init__(self):
        self.demande_service = DemandeService()
    
    def get_all_demandes(self):
        return self.demande_service.get_all_demandes()
    
    def get_demande_by_id(self, demande_id):
        return self.demande_service.get_demande_by_id(demande_id)
    
    def get_demande_by_numero(self, numero):
        return self.demande_service.get_demande_by_numero(numero)
    
    def create_demande(self, demande_data):
        return self.demande_service.create_demande(demande_data)
    
    def update_demande(self, demande_id, demande_data):
        return self.demande_service.update_demande(demande_id, demande_data)
    
    def delete_demande(self, demande_id):
        return self.demande_service.delete_demande(demande_id)
    
    def get_demandes_by_statut(self, statut):
        return self.demande_service.get_demandes_by_statut(statut)
    
    def get_demandes_by_type(self, type_id):
        return self.demande_service.get_demandes_by_type(type_id)
    
    def get_demandes_by_utilisateur(self, utilisateur_id):
        return self.demande_service.get_demandes_by_utilisateur(utilisateur_id)
    
    def get_demandes_by_entite(self, entite_id):
        return self.demande_service.get_demandes_by_entite(entite_id)
    
    def get_demandes_by_priorite(self, niveau_priorite):
        return self.demande_service.get_demandes_by_priorite(niveau_priorite)
    
    def prendre_en_charge_demande(self, demande_id, utilisateur_id):
        return self.demande_service.prendre_en_charge_demande(demande_id, utilisateur_id)
    
    def terminer_demande(self, demande_id):
        return self.demande_service.terminer_demande(demande_id)
    
    def search_demandes(self, search_term):
        return self.demande_service.search_demandes(search_term) 