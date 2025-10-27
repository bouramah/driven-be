from app.common.models import Utilisateur, UtilisateurRole, Role, Application, Entite, Settings, Objectif, db
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload

class UtilisateurService:
    def get_utilisateurs_paginated(self, page, per_page):
        """Lister tous les utilisateurs avec pagination"""
        return Utilisateur.query.options(
            joinedload(Utilisateur.utilisateur_roles).joinedload(UtilisateurRole.application)
        ).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_utilisateurs_by_entite_paginated(self, entite_id, page, per_page):
        """Lister tous les utilisateurs d'une entité avec pagination"""
        return Utilisateur.query.options(
            joinedload(Utilisateur.utilisateur_roles).joinedload(UtilisateurRole.application)
        ).filter_by(id_entite=entite_id).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_utilisateurs_by_role_paginated(self, role_id, page, per_page):
        """Lister tous les utilisateurs ayant un rôle spécifique avec pagination"""
        # Récupérer les IDs des utilisateurs ayant ce rôle
        user_ids = db.session.query(UtilisateurRole.id_utilisateur).filter_by(role_id=role_id).distinct().all()
        user_ids = [id[0] for id in user_ids]  # Convertir les tuples en liste simple
        
        # Récupérer les utilisateurs correspondants
        return Utilisateur.query.filter(Utilisateur.id_utilisateur.in_(user_ids)).paginate(page=page, per_page=per_page, error_out=False)
    
    def get_utilisateur_by_id(self, utilisateur_id):
        """Récupérer un utilisateur par son ID"""
        return Utilisateur.query.options(
            joinedload(Utilisateur.utilisateur_roles).joinedload(UtilisateurRole.application)
        ).get(utilisateur_id)
    
    def get_utilisateur_by_login(self, login):
        """Récupérer un utilisateur par son login"""
        return Utilisateur.query.options(
            joinedload(Utilisateur.utilisateur_roles).joinedload(UtilisateurRole.application)
        ).filter_by(login=login).first()
    
    def get_utilisateur_by_email(self, email):
        """Récupérer un utilisateur par son email"""
        return Utilisateur.query.options(
            joinedload(Utilisateur.utilisateur_roles).joinedload(UtilisateurRole.application)
        ).filter_by(email=email).first()
    
    def create_utilisateur(self, utilisateur_data):
        """Créer un nouvel utilisateur"""
        try:
            # Vérifier que l'entité existe
            if 'id_entite' not in utilisateur_data:
                raise ValueError("L'ID de l'entité est requis pour créer un utilisateur")
            
            entite = Entite.query.get(utilisateur_data['id_entite'])
            if not entite:
                raise ValueError(f"L'entité avec l'ID {utilisateur_data['id_entite']} n'existe pas")
            
            # Vérifier si un utilisateur avec le même login ou email existe déjà
            existing_user = Utilisateur.query.filter(
                or_(
                    Utilisateur.login == utilisateur_data['login'],
                    Utilisateur.email == utilisateur_data['email']
                )
            ).first()
            
            if existing_user:
                if existing_user.login == utilisateur_data['login']:
                    raise ValueError(f"Un utilisateur avec le login '{utilisateur_data['login']}' existe déjà")
                else:
                    raise ValueError(f"Un utilisateur avec l'email '{utilisateur_data['email']}' existe déjà")
            
            # Gérer la date d'expiration
            if 'date_expiration' in utilisateur_data:
                if not utilisateur_data['date_expiration'] or utilisateur_data['date_expiration'] == '':
                    utilisateur_data['date_expiration'] = None
                elif isinstance(utilisateur_data['date_expiration'], str):
                    utilisateur_data['date_expiration'] = datetime.fromisoformat(utilisateur_data['date_expiration'].replace('T', ' '))
            
            
            # Créer l'utilisateur
            utilisateur = Utilisateur(**utilisateur_data)
            db.session.add(utilisateur)
            db.session.commit()
            return utilisateur
            
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            db.session.rollback()
            raise
    
    def update_utilisateur(self, utilisateur_id, utilisateur_data):
        """Mettre à jour un utilisateur"""
        try:
            utilisateur = self.get_utilisateur_by_id(utilisateur_id)
            if not utilisateur:
                return None
            
            # Si on change l'entité, vérifier qu'elle existe
            if 'id_entite' in utilisateur_data and utilisateur_data['id_entite'] != utilisateur.id_entite:
                entite = Entite.query.get(utilisateur_data['id_entite'])
                if not entite:
                    raise ValueError(f"L'entité avec l'ID {utilisateur_data['id_entite']} n'existe pas")
            
            # Si on change le login ou l'email, vérifier qu'ils n'existent pas déjà
            if ('login' in utilisateur_data and utilisateur_data['login'] != utilisateur.login) or \
               ('email' in utilisateur_data and utilisateur_data['email'] != utilisateur.email):
                
                filters = []
                if 'login' in utilisateur_data and utilisateur_data['login'] != utilisateur.login:
                    filters.append(Utilisateur.login == utilisateur_data['login'])
                
                if 'email' in utilisateur_data and utilisateur_data['email'] != utilisateur.email:
                    filters.append(Utilisateur.email == utilisateur_data['email'])
                
                existing_user = Utilisateur.query.filter(
                    and_(
                        or_(*filters),
                        Utilisateur.id_utilisateur != utilisateur_id
                    )
                ).first()
                
                if existing_user:
                    if 'login' in utilisateur_data and existing_user.login == utilisateur_data['login']:
                        raise ValueError(f"Un utilisateur avec le login '{utilisateur_data['login']}' existe déjà")
                    else:
                        raise ValueError(f"Un utilisateur avec l'email '{utilisateur_data['email']}' existe déjà")
            
            # Mettre à jour l'utilisateur
            for key, value in utilisateur_data.items():
                setattr(utilisateur, key, value)
                
            db.session.commit()
            return utilisateur
            
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            db.session.rollback()
            raise
    
    def delete_utilisateur(self, utilisateur_id):
        """Supprimer un utilisateur"""
        try:
            utilisateur = self.get_utilisateur_by_id(utilisateur_id)
            if not utilisateur:
                return False
            
            # Supprimer toutes les associations de rôles
            UtilisateurRole.query.filter_by(id_utilisateur=utilisateur_id).delete()
            
            # Supprimer les settings de l'utilisateur
            Settings.query.filter_by(id_utilisateur=utilisateur_id).delete()
            
            # Supprimer les objectifs de l'utilisateur
            Objectif.query.filter_by(id_utilisateur=utilisateur_id).delete()
            
            # Supprimer l'utilisateur
            db.session.delete(utilisateur)
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            db.session.rollback()
            raise
    
    def prolonger_date_expiration(self, utilisateur_id, nouvelle_date_expiration=None):
        """
        Prolonge la date d'expiration d'un utilisateur.
        
        Args:
            utilisateur_id (int): L'ID de l'utilisateur
            nouvelle_date_expiration (str ou datetime): La nouvelle date d'expiration
                Si None, la date sera prolongée de 30 jours par défaut
        
        Returns:
            dict: Les informations de l'utilisateur mis à jour
        """
        utilisateur = self.get_utilisateur_by_id(utilisateur_id)
        if not utilisateur:
            return None
        
        if nouvelle_date_expiration:
            # Convertir la chaîne de date en objet datetime si nécessaire
            if isinstance(nouvelle_date_expiration, str):
                nouvelle_date_expiration = datetime.fromisoformat(nouvelle_date_expiration.replace('T', ' '))
        else:
            # Comportement par défaut: prolonger de 30 jours
            nouvelle_date_expiration = datetime.now() + timedelta(days=30)
        
        # Mise à jour de la date d'expiration
        utilisateur.date_expiration = nouvelle_date_expiration
        
        # Enregistrer les modifications
        db.session.commit()
        
        return utilisateur
    
    def update_profil(self, utilisateur_id, profil_data):
        """Mettre à jour le profil d'un utilisateur"""
        try:
            # Seuls certains champs peuvent être mis à jour via cette méthode
            allowed_fields = ['nom', 'prenom', 'email']
            filtered_data = {k: v for k, v in profil_data.items() if k in allowed_fields}
            
            return self.update_utilisateur(utilisateur_id, filtered_data)
            
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            raise
    
    def update_statut(self, utilisateur_id, statut):
        """Mettre à jour le statut d'un utilisateur (actif, inactif, etc.)"""
        try:
            utilisateur = self.get_utilisateur_by_id(utilisateur_id)
            if not utilisateur:
                return None
            
            # Vérifier que le statut est valide
            statuts_valides = ['Actif', 'Inactif', 'Suspendu', 'En attente']
            if statut not in statuts_valides:
                raise ValueError(f"Statut invalide. Les statuts valides sont: {', '.join(statuts_valides)}")
            
            # Mettre à jour le statut
            utilisateur.statut = statut
            db.session.commit()
            return utilisateur
            
        except Exception as e:
            print(f"Error updating status: {str(e)}")
            db.session.rollback()
            raise
    
    def verifier_eligibilite(self, utilisateur_id, app_id=None):
        """
        Vérifier l'éligibilité d'un utilisateur (date d'expiration, statut)
        Optionnellement, vérifier s'il a accès à une application spécifique
        """
        try:
            utilisateur = self.get_utilisateur_by_id(utilisateur_id)
            if not utilisateur:
                return {
                    'eligible': False,
                    'raison': 'Utilisateur non trouvé'
                }
            
            # Vérifier la date d'expiration
            if utilisateur.date_expiration < datetime.utcnow():
                return {
                    'eligible': False,
                    'raison': 'Compte expiré'
                }
            
            # Vérifier le statut
            if utilisateur.statut != 'Actif':
                return {
                    'eligible': False,
                    'raison': f'Compte {utilisateur.statut.lower()}'
                }
            
            # Si un app_id est spécifié, vérifier si l'utilisateur a accès à cette application
            if app_id:
                user_roles = UtilisateurRole.query.filter_by(
                    id_utilisateur=utilisateur_id,
                    app_id=app_id
                ).first()
                
                if not user_roles:
                    return {
                        'eligible': False,
                        'raison': 'Aucun rôle pour cette application'
                    }
            
            return {
                'eligible': True,
                'raison': None
            }
            
        except Exception as e:
            print(f"Error checking eligibility: {str(e)}")
            raise
    
    def assign_role(self, utilisateur_id, role_id, creer_par, modifier_par):
        """Assigner un rôle à un utilisateur"""
        try:
            # Vérifier que l'utilisateur existe
            utilisateur = self.get_utilisateur_by_id(utilisateur_id)
            if not utilisateur:
                raise ValueError(f"L'utilisateur avec l'ID {utilisateur_id} n'existe pas")
            
            # Vérifier que le rôle existe et récupérer son app_id
            role = Role.query.get(role_id)
            if not role:
                raise ValueError(f"Le rôle avec l'ID {role_id} n'existe pas")
            
            # Vérifier si l'association existe déjà
            existing_role = UtilisateurRole.query.filter_by(
                id_utilisateur=utilisateur_id,
                role_id=role_id,
                app_id=role.app_id
            ).first()
            
            if existing_role:
                return existing_role
            
            # Créer l'association
            utilisateur_role = UtilisateurRole(
                id_utilisateur=utilisateur_id,
                role_id=role_id,
                app_id=role.app_id,
                creer_par=creer_par,
                modifier_par=modifier_par
            )
            
            db.session.add(utilisateur_role)
            db.session.commit()
            return utilisateur_role
            
        except Exception as e:
            print(f"Error assigning role: {str(e)}")
            db.session.rollback()
            raise
    
    def assign_multiple_roles(self, utilisateur_id, role_ids, creer_par, modifier_par):
        """Assigner plusieurs rôles à un utilisateur en une seule transaction"""
        try:
            # Vérifier que l'utilisateur existe
            utilisateur = self.get_utilisateur_by_id(utilisateur_id)
            if not utilisateur:
                raise ValueError(f"L'utilisateur avec l'ID {utilisateur_id} n'existe pas")
            
            # Récupérer tous les rôles
            roles = Role.query.filter(Role.role_id.in_(role_ids)).all()
            if len(roles) != len(role_ids):
                missing_roles = set(role_ids) - set(role.role_id for role in roles)
                raise ValueError(f"Les rôles suivants n'existent pas : {missing_roles}")
            
            # Récupérer les associations existantes pour tous les rôles
            existing_roles = UtilisateurRole.query.filter(
                UtilisateurRole.id_utilisateur == utilisateur_id,
                UtilisateurRole.role_id.in_(role_ids)
            ).all()
            existing_role_ids = {ur.role_id for ur in existing_roles}
            
            # Créer les nouvelles associations
            new_roles = []
            for role in roles:
                if role.role_id not in existing_role_ids:
                    utilisateur_role = UtilisateurRole(
                        id_utilisateur=utilisateur_id,
                        role_id=role.role_id,
                        app_id=role.app_id,
                        creer_par=creer_par,
                        modifier_par=modifier_par
                    )
                    db.session.add(utilisateur_role)
                    new_roles.append(utilisateur_role)
            
            if new_roles:
                db.session.commit()
            
            # Retourner toutes les associations (nouvelles et existantes)
            return existing_roles + new_roles
            
        except Exception as e:
            print(f"Error assigning multiple roles: {str(e)}")
            db.session.rollback()
            raise
    
    def remove_role(self, utilisateur_id, role_id, app_id):
        """Retirer un rôle à un utilisateur"""
        try:
            # Supprimer l'association
            result = UtilisateurRole.query.filter_by(
                id_utilisateur=utilisateur_id,
                role_id=role_id,
                app_id=app_id
            ).delete()
            
            db.session.commit()
            return result > 0
            
        except Exception as e:
            print(f"Error removing role: {str(e)}")
            db.session.rollback()
            raise
    
    def get_utilisateur_roles(self, utilisateur_id):
        """Récupérer tous les rôles d'un utilisateur"""
        try:
            return UtilisateurRole.query.filter_by(id_utilisateur=utilisateur_id).all()
            
        except Exception as e:
            print(f"Error getting user roles: {str(e)}")
            raise
