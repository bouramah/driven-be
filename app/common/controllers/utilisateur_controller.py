from app.common.services.utilisateur_service import UtilisateurService

class UtilisateurController:
    def __init__(self):
        self.utilisateur_service = UtilisateurService()
    
    def get_utilisateurs_paginated(self, page, per_page):
        """Lister tous les utilisateurs avec pagination"""
        return self.utilisateur_service.get_utilisateurs_paginated(page, per_page)
    
    def get_utilisateurs_by_entite_paginated(self, entite_id, page, per_page):
        """Lister tous les utilisateurs d'une entité avec pagination"""
        return self.utilisateur_service.get_utilisateurs_by_entite_paginated(entite_id, page, per_page)
    
    def get_utilisateurs_by_role_paginated(self, role_id, page, per_page):
        """Lister tous les utilisateurs ayant un rôle spécifique avec pagination"""
        return self.utilisateur_service.get_utilisateurs_by_role_paginated(role_id, page, per_page)
    
    def get_utilisateur_by_id(self, utilisateur_id):
        """Récupérer un utilisateur par son ID"""
        return self.utilisateur_service.get_utilisateur_by_id(utilisateur_id)
    
    def get_utilisateur_by_login(self, login):
        """Récupérer un utilisateur par son login"""
        return self.utilisateur_service.get_utilisateur_by_login(login)
    
    def get_utilisateur_by_email(self, email):
        """Récupérer un utilisateur par son email"""
        return self.utilisateur_service.get_utilisateur_by_email(email)
    
    def create_utilisateur(self, utilisateur_data):
        """Créer un nouvel utilisateur"""
        return self.utilisateur_service.create_utilisateur(utilisateur_data)
    
    def update_utilisateur(self, utilisateur_id, utilisateur_data):
        """Mettre à jour un utilisateur"""
        return self.utilisateur_service.update_utilisateur(utilisateur_id, utilisateur_data)
    
    def delete_utilisateur(self, utilisateur_id):
        """Supprimer un utilisateur"""
        return self.utilisateur_service.delete_utilisateur(utilisateur_id)
    
    def prolonger_date_expiration(self, utilisateur_id, jours=30):
        """Prolonger la date d'expiration d'un utilisateur"""
        return self.utilisateur_service.prolonger_date_expiration(utilisateur_id, jours)
    
    def update_profil(self, utilisateur_id, profil_data):
        """Mettre à jour le profil d'un utilisateur"""
        return self.utilisateur_service.update_profil(utilisateur_id, profil_data)
    
    def update_statut(self, utilisateur_id, statut):
        """Mettre à jour le statut d'un utilisateur"""
        return self.utilisateur_service.update_statut(utilisateur_id, statut)
    
    def verifier_eligibilite(self, utilisateur_id, app_id=None):
        """Vérifier l'éligibilité d'un utilisateur"""
        return self.utilisateur_service.verifier_eligibilite(utilisateur_id, app_id)
    
    def assign_role(self, utilisateur_id, role_id, creer_par, modifier_par):
        """Assigner un rôle à un utilisateur"""
        return self.utilisateur_service.assign_role(utilisateur_id, role_id, creer_par, modifier_par)
    
    def assign_multiple_roles(self, utilisateur_id, role_ids, creer_par, modifier_par):
        """Assigner plusieurs rôles à un utilisateur"""
        return self.utilisateur_service.assign_multiple_roles(utilisateur_id, role_ids, creer_par, modifier_par)
    
    def remove_role(self, utilisateur_id, role_id, app_id):
        """Retirer un rôle à un utilisateur"""
        return self.utilisateur_service.remove_role(utilisateur_id, role_id, app_id)
    
    def get_utilisateur_roles(self, utilisateur_id):
        """Récupérer tous les rôles d'un utilisateur"""
        return self.utilisateur_service.get_utilisateur_roles(utilisateur_id)
    
