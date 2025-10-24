from app.common.services.auth_service import AuthService

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def login(self, login, password):
        """
        Gère le processus d'authentification
        """
        result, status = self.auth_service.authenticate_user(login, password)
        
        error_messages = {
            "user_not_found": {
                "en": "User not found",
                "fr": "Utilisateur non trouvé"
            },
            "inactive_account": {
                "en": "Account is inactive",
                "fr": "Compte inactif"
            },
            "expired_account": {
                "en": "Account has expired",
                "fr": "Compte expiré"
            },
            "ldap_error": {
                "en": "LDAP authentication service error",
                "fr": "Erreur du service d'authentification LDAP"
            },
            "invalid_credentials": {
                "en": "Invalid credentials",
                "fr": "Identifiants invalides"
            },
            "system_error": {
                "en": "System error during authentication",
                "fr": "Erreur système lors de l'authentification"
            }
        }

        if status != "success":
            return {
                "error": True,
                "message": error_messages.get(status, {
                    "en": "Unknown error",
                    "fr": "Erreur inconnue"
                })
            }, self._get_status_code(status)

        return {
            "error": False,
            "message": {
                "en": "Authentication successful",
                "fr": "Authentification réussie"
            },
            "data": {
                "access_token": result["access_token"],
                "utilisateur": result["utilisateur"]
            }
        }, 200

    def _get_status_code(self, status):
        """
        Détermine le code HTTP approprié selon le statut
        """
        status_codes = {
            "user_not_found": 404,
            "inactive_account": 403,
            "expired_account": 403,
            "ldap_error": 500,
            "invalid_credentials": 401,
            "system_error": 500
        }
        return status_codes.get(status, 500) 