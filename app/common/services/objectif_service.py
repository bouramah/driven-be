from app.common.models import Objectif, Utilisateur, UtilisateurRole, Role, db
from sqlalchemy.orm import joinedload
from datetime import datetime

class ObjectifService:
    def _is_admin_user(self, user_id):
        """Vérifier si l'utilisateur a un profil administrateur"""
        user = Utilisateur.query.get(user_id)
        if not user:
            return False
        
        # Vérifier si l'utilisateur a un profil 'Administrateur'
        return user.profil == 'Administrateur'
    
    def _get_users_in_same_entity(self, user_id):
        """Récupérer les utilisateurs de la même entité"""
        user = Utilisateur.query.get(user_id)
        if not user:
            return []
        
        # Récupérer tous les utilisateurs de la même entité
        users_in_entity = Utilisateur.query.filter_by(id_entite=user.id_entite).all()
        return [u.id_utilisateur for u in users_in_entity]
    
    def _can_assign_objectif_to_user(self, current_user_id, target_user_id):
        """Vérifier si l'utilisateur courant peut assigner un objectif à l'utilisateur cible"""
        if self._is_admin_user(current_user_id):
            return True  # Admin peut assigner à n'importe qui
        
        # Utilisateur normal ne peut assigner qu'aux membres de son entité
        users_in_entity = self._get_users_in_same_entity(current_user_id)
        return target_user_id in users_in_entity
    
    def get_all_objectifs(self):
        return Objectif.query.options(
            joinedload(Objectif.utilisateur),
            joinedload(Objectif.application)
        ).all()
    
    def get_all_objectifs_paginated(self, page, per_page):
        pagination = Objectif.query.options(
            joinedload(Objectif.utilisateur),
            joinedload(Objectif.application)
        ).paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total
    
    def get_objectifs_for_user(self, current_user_id, page=1, per_page=10):
        """Récupérer les objectifs selon les permissions de l'utilisateur"""
        if self._is_admin_user(current_user_id):
            # Admin peut voir tous les objectifs
            pagination = Objectif.query.options(
                joinedload(Objectif.utilisateur),
                joinedload(Objectif.application)
            ).paginate(page=page, per_page=per_page, error_out=False)
        else:
            # Utilisateur normal ne peut voir que les objectifs des membres de son entité
            users_in_entity = self._get_users_in_same_entity(current_user_id)
            pagination = Objectif.query.options(
                joinedload(Objectif.utilisateur),
                joinedload(Objectif.application)
            ).filter(Objectif.id_utilisateur.in_(users_in_entity)).paginate(
                page=page, per_page=per_page, error_out=False
            )
        
        return pagination.items, pagination.pages, pagination.total
    
    def get_available_users_for_objectif(self, current_user_id):
        """Récupérer les utilisateurs auxquels on peut assigner des objectifs"""
        if self._is_admin_user(current_user_id):
            # Admin peut assigner à n'importe qui
            return Utilisateur.query.options(joinedload(Utilisateur.entite)).all()
        else:
            # Utilisateur normal ne peut assigner qu'aux membres de son entité
            users_in_entity = self._get_users_in_same_entity(current_user_id)
            return Utilisateur.query.options(joinedload(Utilisateur.entite)).filter(
                Utilisateur.id_utilisateur.in_(users_in_entity)
            ).all()
    
    def get_objectif_by_id(self, objectif_id):
        return Objectif.query.options(
            joinedload(Objectif.utilisateur),
            joinedload(Objectif.application)
        ).get(objectif_id)
    
    def get_objectifs_by_utilisateur(self, utilisateur_id):
        return Objectif.query.filter_by(id_utilisateur=utilisateur_id).all()
    
    def get_objectifs_by_utilisateur_paginated(self, utilisateur_id, page, per_page):
        pagination = Objectif.query.filter_by(id_utilisateur=utilisateur_id).paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.pages, pagination.total
    
    def create_objectif(self, objectif_data, current_user_id):
        """Créer un objectif avec validation des permissions"""
        target_user_id = objectif_data.get('id_utilisateur')
        
        # Vérifier les permissions
        if not self._can_assign_objectif_to_user(current_user_id, target_user_id):
            raise ValueError({
                "fr": "Vous n'avez pas les permissions pour assigner un objectif à cet utilisateur",
                "en": "You don't have permission to assign an objective to this user"
            })
        
        # Convertir les dates de chaînes vers datetime si nécessaire
        date_fields = ['date_debut', 'date_fin']
        for field in date_fields:
            if field in objectif_data and isinstance(objectif_data[field], str):
                try:
                    # Parser la date depuis le format 'YYYY-MM-DD'
                    objectif_data[field] = datetime.strptime(objectif_data[field], '%Y-%m-%d')
                except ValueError:
                    # Si le format est différent, essayer le format ISO
                    try:
                        objectif_data[field] = datetime.fromisoformat(objectif_data[field].replace('Z', '+00:00'))
                    except ValueError:
                        # Si ça ne marche toujours pas, lever une erreur
                        raise ValueError(f"Format de date invalide pour {field}: {objectif_data[field]}")
        
        objectif = Objectif(**objectif_data)
        db.session.add(objectif)
        db.session.commit()
        return self.get_objectif_by_id(objectif.id)  # Retourner avec les relations chargées
    
    def update_objectif(self, objectif_id, objectif_data, current_user_id):
        """Mettre à jour un objectif avec validation des permissions"""
        objectif = self.get_objectif_by_id(objectif_id)
        if not objectif:
            return None
        
        # Si on change l'utilisateur assigné, vérifier les permissions
        if 'id_utilisateur' in objectif_data:
            new_target_user_id = objectif_data['id_utilisateur']
            if not self._can_assign_objectif_to_user(current_user_id, new_target_user_id):
                raise ValueError({
                    "fr": "Vous n'avez pas les permissions pour assigner un objectif à cet utilisateur",
                    "en": "You don't have permission to assign an objective to this user"
                })
        
        # Convertir les dates de chaînes vers datetime si nécessaire
        date_fields = ['date_debut', 'date_fin']
        for field in date_fields:
            if field in objectif_data and isinstance(objectif_data[field], str):
                try:
                    # Parser la date depuis le format 'YYYY-MM-DD'
                    objectif_data[field] = datetime.strptime(objectif_data[field], '%Y-%m-%d')
                except ValueError:
                    # Si le format est différent, essayer le format ISO
                    try:
                        objectif_data[field] = datetime.fromisoformat(objectif_data[field].replace('Z', '+00:00'))
                    except ValueError:
                        # Si ça ne marche toujours pas, lever une erreur
                        raise ValueError(f"Format de date invalide pour {field}: {objectif_data[field]}")
            
        for key, value in objectif_data.items():
            setattr(objectif, key, value)
            
        db.session.commit()
        return self.get_objectif_by_id(objectif_id)  # Retourner avec les relations chargées
    
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