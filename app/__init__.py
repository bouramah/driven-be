from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from app.config import get_config
from datetime import timedelta

# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()

class Application:
    def __init__(self, config_class=None):
        """Constructeur de l'application"""
        self.app = Flask(__name__)
        
        # Charger la configuration
        if config_class is None:
            config_class = get_config()
        self.app.config.from_object(config_class)
        
        # Initialiser les extensions
        self.init_extensions()
        
        # Enregistrer les blueprints
        self.register_blueprints()
    
    def init_extensions(self):
        """Initialise les extensions Flask avec l'application"""
        db.init_app(self.app)
        migrate.init_app(self.app, db)
        self.configure_jwt()
        ma.init_app(self.app)
        
        # Créer les tables dans un contexte d'application
        with self.app.app_context():
            db.create_all()
        
        # Configuration CORS
        CORS(self.app, resources={
            r"/api/*": {
                "origins": self.app.config['CORS_ORIGINS'],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })
    
    def configure_jwt(self):
        # Configuration JWT
        self.jwt = JWTManager(self.app)
        
        @self.jwt.invalid_token_loader
        def custom_invalid_token_callback(error):
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Invalid token',
                    'fr': 'Token invalide'
                },
                'details': str(error)
            }), 401

        @self.jwt.expired_token_loader
        def custom_expired_token_callback(jwt_header, jwt_payload):
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Token has expired',
                    'fr': 'Token expiré'
                },
                'details': {
                    'en': 'Please login again to get a new token',
                    'fr': 'Connectez-vous à nouveau pour obtenir un nouveau token'
                }
            }), 401

        @self.jwt.unauthorized_loader
        def custom_unauthorized_callback(error):
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Unauthorized access',
                    'fr': 'Accès non autorisé'
                },
                'details': str(error)
            }), 401

        @self.jwt.needs_fresh_token_loader
        def custom_needs_fresh_token_callback(jwt_header, jwt_payload):
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Fresh token required',
                    'fr': 'Token non frais'
                },
                'details': {
                    'en': 'A fresh token is required',
                    'fr': 'Un token frais est nécessaire'
                }
            }), 401

        @self.jwt.revoked_token_loader
        def custom_revoked_token_callback(jwt_header, jwt_payload):
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Token has been revoked',
                    'fr': 'Token révoqué'
                },
                'details': {
                    'en': 'The token has been revoked',
                    'fr': 'Le token a été révoqué'
                }
            }), 401

        @self.jwt.token_verification_failed_loader
        def custom_token_verification_failed_callback(jwt_header, jwt_payload):
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Token verification failed',
                    'fr': 'Échec de la vérification du token'
                },
                'details': {
                    'en': 'Token verification process failed',
                    'fr': 'Le processus de vérification du token a échoué'
                }
            }), 401

        # Configuration JWT
        self.app.config['JWT_SECRET_KEY'] = self.app.config['SECRET_KEY']
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
        self.app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    def register_blueprints(self):
        """Enregistre tous les blueprints de l'application"""
        # Blueprints communs
        
        from app.common.routes.auth import auth_bp
        self.app.register_blueprint(auth_bp, url_prefix='/api/auth')


        from app.common.routes.roles import role_bp
        self.app.register_blueprint(role_bp, url_prefix='/api/roles')
           
        from app.common.routes.permissions import permission_bp
        self.app.register_blueprint(permission_bp, url_prefix='/api/permissions')
        
        from app.common.routes.permission_page import permission_page_bp
        self.app.register_blueprint(permission_page_bp, url_prefix='/api/permissions_page')
        
        from app.common.routes.fonctions_api import fonction_api_bp
        self.app.register_blueprint(fonction_api_bp, url_prefix='/api/fonctions_api')
        
        from app.common.routes.trace import trace_bp
        self.app.register_blueprint(trace_bp, url_prefix='/api/traces')
        
        from app.common.routes.page import page_bp
        self.app.register_blueprint(page_bp, url_prefix='/api/pages')
        
        from app.common.routes.application import application_bp
        self.app.register_blueprint(application_bp, url_prefix='/api/applications')
        
        from app.common.routes.entite import entite_bp
        self.app.register_blueprint(entite_bp, url_prefix='/api/entites')
        
        from app.common.routes.utilisateur import utilisateur_bp
        self.app.register_blueprint(utilisateur_bp, url_prefix='/api/utilisateurs')
        
        from app.common.routes.blacklist import blacklist_bp
        self.app.register_blueprint(blacklist_bp, url_prefix='/api/blacklist')
        
        from app.common.routes.codification import codification_bp
        self.app.register_blueprint(codification_bp, url_prefix='/api/codifications')
        
        from app.common.routes.settings import settings_bp
        self.app.register_blueprint(settings_bp, url_prefix='/api/settings')
        
        from app.common.routes.objectif import objectif_bp
        self.app.register_blueprint(objectif_bp, url_prefix='/api/objectifs')
                
        # Blueprints des applications
        from app.apps.gestion_demande.demande import demande_bp
        self.app.register_blueprint(demande_bp, url_prefix='/api/demandes')
        
        from app.apps.gestion_demande.type_demande import type_demande_bp
        self.app.register_blueprint(type_demande_bp, url_prefix='/api/type_demandes')
        
        # Blueprints KPI et consultation
        try:
            from app.apps.kpi_dde.routes import kpi_bp
            self.app.register_blueprint(kpi_bp, url_prefix='/api/kpi')
        except ImportError:
            pass
            
        try:
            from app.apps.consultation.routes import consultation_bp
            self.app.register_blueprint(consultation_bp, url_prefix='/api/consultation')
        except ImportError:
            pass
    
    def get_app(self):
        """Retourne l'instance de l'application Flask"""
        return self.app

# Fonction de compatibilité pour maintenir l'API existante
def create_app(config_class=None):
    """Crée et configure l'application Flask"""
    application = Application(config_class)
    return application.get_app()
