from datetime import datetime, timedelta
import requests
from flask_jwt_extended import create_access_token
from app.common.models import Utilisateur, db

class AuthService:
    def authenticate_user(self, login, password):
        """
        Authentifie un utilisateur via LDAP et génère un token JWT
        """
        try:
            # Vérifier si l'utilisateur existe
            utilisateur = Utilisateur.query.filter_by(login=login).first()
            if not utilisateur:
                return None, "user_not_found"

            # Vérifier le statut et la date d'expiration
            if utilisateur.statut != 'Actif':
                return None, "inactive_account"
            
            if utilisateur.date_expiration and utilisateur.date_expiration < datetime.utcnow():
                return None, "expired_account"

            # Authentification LDAP
            ldap_api_url = "http://10.173.69.41:6003/auth"
            ldap_response = requests.post(ldap_api_url, json={
                "login": login,
                "password": password
            })

            if ldap_response.status_code != 200:
                return None, "ldap_error"

            ldap_data = ldap_response.json()
            if ldap_data['code'] != '200':
                return None, "invalid_credentials"

            # Création du token JWT
            additional_claims = {
                "profil": utilisateur.profil,
                "id_utilisateur": utilisateur.id_utilisateur,
                "id_entite": utilisateur.id_entite
            }

            access_token = create_access_token(
                identity=login,
                expires_delta=timedelta(days=1),
                additional_claims=additional_claims
            )

            return {
                "access_token": access_token,
                "utilisateur": utilisateur
            }, "success"

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None, "system_error" 