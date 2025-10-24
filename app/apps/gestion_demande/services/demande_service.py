from app.apps.gestion_demande.models import Demande, db
from datetime import datetime

class DemandeService:
    def get_all_demandes(self):
        return Demande.query.all()
    
    def get_demande_by_id(self, demande_id):
        return Demande.query.get(demande_id)
    
    def get_demande_by_numero(self, numero):
        return Demande.query.filter_by(numero_demande=numero).first()
    
    def create_demande(self, demande_data):
        demande = Demande(**demande_data)
        if 'date_initiation' not in demande_data:
            demande.date_initiation = datetime.utcnow()
        demande.statut = 'Initié'
            
        db.session.add(demande)
        db.session.commit()
        return demande
    
    def update_demande(self, demande_id, demande_data):
        demande = self.get_demande_by_id(demande_id)
        if not demande:
            return None
            
        for key, value in demande_data.items():
            setattr(demande, key, value)
            
        db.session.commit()
        return demande
    
    def delete_demande(self, demande_id):
        demande = self.get_demande_by_id(demande_id)
        if demande:
            db.session.delete(demande)
            db.session.commit()
            return True
        return False
    
    def get_demandes_by_statut(self, statut):
        return Demande.query.filter_by(statut=statut).all()
    
    def get_demandes_by_type(self, type_id):
        return Demande.query.filter_by(id_type=type_id).all()
    
    def get_demandes_by_utilisateur(self, utilisateur_id):
        return Demande.query.filter_by(id_utilisateur=utilisateur_id).all()
    
    def get_demandes_by_entite(self, entite_id):
        return Demande.query.filter_by(id_entite=entite_id).all()
    
    def get_demandes_by_priorite(self, niveau_priorite):
        return Demande.query.filter_by(niveau_priorite=niveau_priorite).all()
    
    def prendre_en_charge_demande(self, demande_id, utilisateur_id):
        demande = self.get_demande_by_id(demande_id)
        if not demande or demande.statut != 'Initié':
            return None
            
        demande.statut = 'Pris en charge'
        demande.id_utilisateur_traiter = utilisateur_id
        demande.date_prise_en_charge = datetime.utcnow()
        db.session.commit()
        return demande
    
    def terminer_demande(self, demande_id):
        demande = self.get_demande_by_id(demande_id)
        if not demande or demande.statut != 'Pris en charge':
            return None
            
        demande.statut = 'Terminé'
        demande.date_fin = datetime.utcnow()
        db.session.commit()
        return demande
    
    def search_demandes(self, search_term):
        return Demande.query.filter(
            (Demande.numero_demande.ilike(f'%{search_term}%')) |
            (Demande.nom.ilike(f'%{search_term}%')) |
            (Demande.description.ilike(f'%{search_term}%'))
        ).all() 