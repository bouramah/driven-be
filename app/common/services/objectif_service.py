from app.common.models import Objectif, db

class ObjectifService:
    def get_all_objectifs(self):
        return Objectif.query.all()
    
    def get_all_objectifs_paginated(self, page, per_page):
        pagination = Objectif.query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total
    
    def get_objectif_by_id(self, objectif_id):
        return Objectif.query.get(objectif_id)
    
    def get_objectifs_by_utilisateur(self, utilisateur_id):
        return Objectif.query.filter_by(id_utilisateur=utilisateur_id).all()
    
    def get_objectifs_by_utilisateur_paginated(self, utilisateur_id, page, per_page):
        pagination = Objectif.query.filter_by(id_utilisateur=utilisateur_id).paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total
    
    def create_objectif(self, objectif_data):
        objectif = Objectif(**objectif_data)
        db.session.add(objectif)
        db.session.commit()
        return objectif
    
    def update_objectif(self, objectif_id, objectif_data):
        objectif = self.get_objectif_by_id(objectif_id)
        if not objectif:
            return None
            
        for key, value in objectif_data.items():
            setattr(objectif, key, value)
            
        db.session.commit()
        return objectif
    
    def delete_objectif(self, objectif_id):
        objectif = self.get_objectif_by_id(objectif_id)
        if objectif:
            db.session.delete(objectif)
            db.session.commit()
            return True
        return False
    
    def get_objectifs_by_type(self, type_objectif):
        return Objectif.query.filter_by(type=type_objectif).all()
    
    def get_objectifs_by_type_paginated(self, type_objectif, page, per_page):
        pagination = Objectif.query.filter_by(type=type_objectif).paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total
    
    def get_objectifs_by_periode(self, periode):
        # Vérifier si la période est une plage (contient un tiret)
        if '-' in periode:
            debut_periode, fin_periode = periode.split('-')
            # Utiliser LIKE pour trouver les objectifs dont la période est dans la plage
            # ou correspond exactement à la plage
            return Objectif.query.filter(
                (Objectif.periode == periode) | 
                (Objectif.periode.like(f"{debut_periode}%")) |
                (Objectif.periode.like(f"%{fin_periode}")) |
                (Objectif.periode.like(f"%-%"))
            ).all()
        else:
            # Si ce n'est pas une plage, rechercher par période exacte ou plages contenant cette période
            return Objectif.query.filter(
                (Objectif.periode == periode) | 
                (Objectif.periode.like(f"%-{periode}")) |
                (Objectif.periode.like(f"{periode}-%")) |
                (Objectif.periode.like(f"%-%"))
            ).all()
    
    def get_objectifs_by_periode_paginated(self, periode, page, per_page):
        # Vérifier si la période est une plage (contient un tiret)
        if '-' in periode:
            debut_periode, fin_periode = periode.split('-')
            # Utiliser LIKE pour trouver les objectifs dont la période est dans la plage
            # ou correspond exactement à la plage
            query = Objectif.query.filter(
                (Objectif.periode == periode) | 
                (Objectif.periode.like(f"{debut_periode}%")) |
                (Objectif.periode.like(f"%{fin_periode}")) |
                (Objectif.periode.like(f"%-%"))
            )
        else:
            # Si ce n'est pas une plage, rechercher par période exacte ou plages contenant cette période
            query = Objectif.query.filter(
                (Objectif.periode == periode) | 
                (Objectif.periode.like(f"%-{periode}")) |
                (Objectif.periode.like(f"{periode}-%")) |
                (Objectif.periode.like(f"%-%"))
            )
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total