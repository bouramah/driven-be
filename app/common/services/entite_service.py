from app.common.models import Entite, db
from sqlalchemy.exc import IntegrityError

class EntiteService:
    def get_all_entites(self):
        return Entite.query.all()
    
    def get_entites_paginated(self, page, per_page):
        return Entite.query.paginate(page=page, per_page=per_page, error_out=False)
    
    def get_entite_by_id(self, entite_id):
        return Entite.query.get(entite_id)
    
    def get_entite_by_code(self, code):
        return Entite.query.filter_by(code=code).first()
    
    def create_entite(self, entite_data):
        try:
            # Vérifier si une entité avec le même nom existe déjà
            existing_name = Entite.query.filter_by(nom=entite_data.get('nom')).first()
            if existing_name:
                raise ValueError("fr:Une entité avec ce nom existe déjà|en:An entity with this name already exists")

            # Vérifier si une entité avec le même code existe déjà
            existing_code = Entite.query.filter_by(code=entite_data.get('code')).first()
            if existing_code:
                raise ValueError("fr:Une entité avec ce code existe déjà|en:An entity with this code already exists")

            entite = Entite(**entite_data)
            db.session.add(entite)
            db.session.commit()
            return entite
        except IntegrityError as e:
            db.session.rollback()
            # Extraire le nom du champ qui cause l'erreur depuis le message
            error_str = str(e.orig)
            if 'email' in error_str:
                raise ValueError("fr:L'email est requis|en:Email is required")
            elif 'nom' in error_str:
                raise ValueError("fr:Le nom est requis|en:Name is required")
            elif 'code' in error_str:
                raise ValueError("fr:Le code est requis|en:Code is required")
            else:
                raise ValueError("fr:Erreur de contrainte de base de données|en:Database constraint error")
    
    def update_entite(self, entite_id, entite_data):
        try:
            entite = self.get_entite_by_id(entite_id)
            if not entite:
                return None
                
            # Si le nom est modifié, vérifier qu'il n'existe pas déjà
            if 'nom' in entite_data and entite_data['nom'] != entite.nom:
                existing_name = Entite.query.filter(
                    Entite.nom == entite_data['nom'],
                    Entite.id != entite_id
                ).first()
                if existing_name:
                    raise ValueError("fr:Une entité avec ce nom existe déjà|en:An entity with this name already exists")

            # Si le code est modifié, vérifier qu'il n'existe pas déjà
            if 'code' in entite_data and entite_data['code'] != entite.code:
                existing_code = Entite.query.filter(
                    Entite.code == entite_data['code'],
                    Entite.id != entite_id
                ).first()
                if existing_code:
                    raise ValueError("fr:Une entité avec ce code existe déjà|en:An entity with this code already exists")

            for key, value in entite_data.items():
                setattr(entite, key, value)
                
            db.session.commit()
            return entite
        except IntegrityError as e:
            db.session.rollback()
            # Extraire le nom du champ qui cause l'erreur depuis le message
            error_str = str(e.orig)
            if 'email' in error_str:
                raise ValueError("fr:L'email est requis|en:Email is required")
            elif 'nom' in error_str:
                raise ValueError("fr:Le nom est requis|en:Name is required")
            elif 'code' in error_str:
                raise ValueError("fr:Le code est requis|en:Code is required")
            else:
                raise ValueError("fr:Erreur de contrainte de base de données|en:Database constraint error")
    
    def delete_entite(self, entite_id):
        entite = self.get_entite_by_id(entite_id)
        if entite:
            db.session.delete(entite)
            db.session.commit()
            return True
        return False 