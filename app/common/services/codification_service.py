from app.common.models import Codification, Settings, db
from sqlalchemy import or_

class CodificationService:
    def get_all_codifications(self):
        return Codification.query.all()
    
    def get_all_codifications_paginated(self, page, per_page):
        pagination = Codification.query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total
    
    def get_codification_by_id(self, codification_id):
        return Codification.query.get(codification_id)
    
    def get_codification_by_param(self, param):
        return Codification.query.filter_by(param=param).first()
    
    def create_codification(self, codification_data):
        # Vérifier si une codification avec le même paramètre ET libellé existe déjà
        existing_codification = Codification.query.filter_by(
            param=codification_data.get('param'),
            libelle=codification_data.get('libelle')
        ).first()
        if existing_codification:
            raise ValueError(f"Une codification avec le paramètre '{codification_data.get('param')}' et le libellé '{codification_data.get('libelle')}' existe déjà")

        codification = Codification(**codification_data)
        db.session.add(codification)
        db.session.commit()
        return codification
    
    def update_codification(self, codification_id, codification_data):
        codification = self.get_codification_by_id(codification_id)
        if not codification:
            return None
            
        # Si le paramètre OU le libellé est modifié, vérifier que la combinaison n'existe pas déjà
        if ('param' in codification_data or 'libelle' in codification_data):
            new_param = codification_data.get('param', codification.param)
            new_libelle = codification_data.get('libelle', codification.libelle)
            
            existing_codification = Codification.query.filter(
                Codification.param == new_param,
                Codification.libelle == new_libelle,
                Codification.id != codification_id
            ).first()
            if existing_codification:
                raise ValueError(f"Une codification avec le paramètre '{new_param}' et le libellé '{new_libelle}' existe déjà")

        for key, value in codification_data.items():
            setattr(codification, key, value)
            
        db.session.commit()
        return codification
    
    def delete_codification(self, codification_id):
        codification = self.get_codification_by_id(codification_id)
        if not codification:
            return False
            
        # Vérifier si la codification est utilisée par des settings
        settings_count = Settings.query.filter_by(id_codification=codification_id).count()
        if settings_count > 0:
            raise ValueError({
                "fr": f"Impossible de supprimer cette codification car elle est utilisée par {settings_count} paramètre(s) utilisateur. Supprimez d'abord les paramètres associés.",
                "en": f"Cannot delete this codification as it is used by {settings_count} user setting(s). Please delete the associated settings first."
            })
            
        db.session.delete(codification)
        db.session.commit()
        return True
    
    def search_codifications(self, search_term):
        return Codification.query.filter(
            or_(
                Codification.libelle.ilike(f'%{search_term}%'),
                Codification.param.ilike(f'%{search_term}%'),
                Codification.description.ilike(f'%{search_term}%')
            )
        ).all()
    
    def search_codifications_paginated(self, search_term, page, per_page):
        pagination = Codification.query.filter(
            or_(
                Codification.libelle.ilike(f'%{search_term}%'),
                Codification.param.ilike(f'%{search_term}%'),
                Codification.description.ilike(f'%{search_term}%')
            )
        ).paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total 