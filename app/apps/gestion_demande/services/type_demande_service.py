from app.apps.gestion_demande.models import TypeDemande, db
from datetime import datetime

class TypeDemandeService:
    def get_all_types_demande(self):
        return TypeDemande.query.all()
    
    def get_type_demande_by_id(self, type_id):
        return TypeDemande.query.get(type_id)
    
    def create_type_demande(self, type_data):
        type_demande = TypeDemande(**type_data)
        db.session.add(type_demande)
        db.session.commit()
        return type_demande
    
    def update_type_demande(self, type_id, type_data):
        type_demande = self.get_type_demande_by_id(type_id)
        if not type_demande:
            return None
            
        for key, value in type_data.items():
            setattr(type_demande, key, value)
            
        db.session.commit()
        return type_demande
    
    def delete_type_demande(self, type_id):
        type_demande = self.get_type_demande_by_id(type_id)
        if type_demande:
            db.session.delete(type_demande)
            db.session.commit()
            return True
        return False 