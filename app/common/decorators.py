from functools import wraps
from flask import request, jsonify, g, current_app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.common.models import FonctionAPI, Utilisateur
from app.common.services.trace_service import TraceService

def require_fonction_permission(nom_fonction):
    """
    Décorateur pour vérifier si l'utilisateur a la permission d'accéder à une fonction API.
    Utilise JWT pour l'authentification au lieu de g.utilisateur.
    
    Args:
        nom_fonction (str): Nom de la fonction API à vérifier
        
    Returns:
        function: Décorateur qui vérifie les permissions
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Vérifier si le token JWT est valide
            try:
                # Cette fonction vérifie si un token JWT valide est présent dans la requête
                # et lève une exception si ce n'est pas le cas
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({
                    'error': True,
                    'message': {
                        'fr': 'Utilisateur non authentifié',
                        'en': 'User not authenticated'
                    },
                    'details': str(e)
                }), 401
            
            # Récupérer l'identité de l'utilisateur à partir du token JWT
            # get_jwt_identity() retourne l'identité stockée dans le token JWT (généralement le login)
            login = get_jwt_identity()
            
            # Récupérer l'utilisateur à partir de la base de données
            utilisateur = Utilisateur.query.filter_by(login=login).first()
            if not utilisateur:
                return jsonify({
                    'error': True,
                    'message': {
                        'fr': 'Utilisateur non trouvé',
                        'en': 'User not found'
                    }
                }), 404
            
            # Récupérer l'ID de l'application depuis la configuration ou les paramètres
            app_id = kwargs.get('app_id') or request.args.get('app_id') or current_app.config.get('DEFAULT_APP_ID')
            
            if not app_id:
                return jsonify({
                    'error': True,
                    'message': {
                        'fr': 'ID de l\'application non spécifié',
                        'en': 'Application ID not specified'
                    }
                }), 400
            
            # Vérifier si l'utilisateur a la permission pour cette fonction
            # La méthode has_permission_for_fonction vérifie si l'utilisateur a un rôle
            # qui possède une permission associée à cette fonction API
            if not utilisateur.has_permission_for_fonction(app_id, nom_fonction):
                current_app.logger.error(f"Accès refusé à {nom_fonction} de l'application {app_id} pour l'utilisateur {utilisateur.login} (ID: {utilisateur.id_utilisateur})")
                return jsonify({
                    'error': True,
                    'message': {
                        'fr': 'Accès non autorisé à cette fonction',
                        'en': 'Unauthorized access to this function'
                    }
                }), 403
            
            # Si l'utilisateur a la permission, exécuter la fonction
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def register_fonction_api(app_id, description=None):
    """
    Décorateur pour enregistrer automatiquement une fonction API dans la base de données.
    Utile lors du développement pour créer automatiquement les fonctions API.
    
    Args:
        app_id (int): ID de l'application
        description (str, optional): Description de la fonction API
        
    Returns:
        function: Décorateur qui enregistre la fonction API
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Récupérer le nom de la fonction
            nom_fonction = f.__name__
            
            # Vérifier si la fonction existe déjà
            fonction = FonctionAPI.query.filter_by(
                nom_fonction=nom_fonction,
                app_id=app_id
            ).first()
            
            # Si la fonction n'existe pas, la créer
            if not fonction:
                from app import db
                
                # Utiliser la docstring de la fonction comme description si non spécifiée
                func_description = description or f.__doc__ or f"Fonction {nom_fonction}"
                
                # Créer la fonction API
                fonction = FonctionAPI(
                    nom_fonction=nom_fonction,
                    description=func_description,
                    app_id=app_id,
                    creer_par=1,  # Utilisateur système par défaut
                    modifier_par=1
                )
                
                db.session.add(fonction)
                db.session.commit()
                
                current_app.logger.info(f"Fonction API '{nom_fonction}' enregistrée automatiquement")
            
            # Exécuter la fonction originale
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

def api_fonction(nom_fonction=None, app_id=None, description=None, auto_register=False):
    """
    Décorateur combiné pour gérer les permissions et l'enregistrement des fonctions API.
    
    Args:
        nom_fonction (str, optional): Nom de la fonction API. Si None, utilise le nom de la fonction Python.
        app_id (int, optional): ID de l'application. Si None, utilise la configuration par défaut.
        description (str, optional): Description de la fonction API.
        auto_register (bool, optional): Si True, enregistre automatiquement la fonction API.
        
    Returns:
        function: Décorateur combiné
    """
    def decorator(f):
        # Utiliser le nom de la fonction Python si nom_fonction n'est pas spécifié
        func_name = nom_fonction or f.__name__
        
        # Appliquer le décorateur de permission
        decorated = require_fonction_permission(func_name)(f)
        
        # Si auto_register est True, appliquer également le décorateur d'enregistrement
        if auto_register and app_id:
            decorated = register_fonction_api(app_id, description)(decorated)
        
        return decorated
    
    return decorator 

def trace_action(action_type, code_prefix):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Récupérer le login de l'utilisateur depuis le JWT
            current_user_login = get_jwt_identity()
            
            # Récupérer l'ID de l'utilisateur à partir du login
            user = Utilisateur.query.filter_by(login=current_user_login).first()
            current_user_id = user.id_utilisateur if user else None       
                 
            # Préparer les paramètres de la trace
            method = request.method
            endpoint = request.path
            params = {
                'method': method,
                'args': kwargs,
                'query_params': dict(request.args),
                'body': request.get_json(silent=True)
            }
            
            # Générer le code unique
            code = f"{code_prefix}_{method}"
            
            # Préparer le détail de l'action
            detail = f"{method} request sur {endpoint}"
            
            try:
                # Exécuter la fonction
                response = f(*args, **kwargs)
                
                # Ajouter le statut de la réponse aux paramètres
                params['status'] = response.status_code if hasattr(response, 'status_code') else 200
                
                # Tracer l'action réussie
                TraceService.ajouter_trace(
                    action=f"{action_type}_{method}",
                    detail=detail,
                    code=code,
                    id_utilisateur=current_user_id,
                    params=params
                )
                
                return response
                
            except Exception as e:
                # Tracer l'erreur
                params['error'] = str(e)
                TraceService.ajouter_trace(
                    action=f"{action_type}_{method}_ERROR",
                    detail=f"Erreur: {str(e)}",
                    code=f"{code}_ERROR",
                    id_utilisateur=current_user_id,
                    params=params
                )
                raise
                
        return decorated_function
    return decorator

def auto_set_user_fields():
    """
    Décorateur pour définir automatiquement les champs creer_par et modifier_par
    en utilisant l'ID de l'utilisateur connecté via JWT.
    
    Ce décorateur doit être utilisé après jwt_required() pour s'assurer que
    l'utilisateur est authentifié.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Récupérer le login de l'utilisateur depuis le JWT
            current_user_login = get_jwt_identity()
            
            # Récupérer l'utilisateur à partir du login
            user = Utilisateur.query.filter_by(login=current_user_login).first()
            if not user:
                return jsonify({
                    'error': True,
                    'message': {
                        'fr': 'Utilisateur non trouvé',
                        'en': 'User not found'
                    }
                }), 404
            
            # Récupérer les données JSON de la requête
            json_data = request.get_json(silent=True) or {}
            
            # Pour les requêtes POST (création), définir creer_par et modifier_par
            if request.method == 'POST':
                json_data['creer_par'] = user.id_utilisateur
                json_data['modifier_par'] = user.id_utilisateur
            
            # Pour les requêtes PUT (modification), définir uniquement modifier_par
            elif request.method in ['PUT', 'PATCH']:
                json_data['modifier_par'] = user.id_utilisateur
            
            # Mettre à jour l'objet request.json avec les nouvelles données
            if hasattr(request, '_cached_json'):
                request._cached_json = (json_data, request._cached_json[1])
            
            # Exécuter la fonction originale
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator

"""
@api_bp.route('/utilisateurs', methods=['GET'])
@api_fonction(app_id=1, auto_register=True)
def get_utilisateurs():
    # Cette fonction sera automatiquement enregistrée avec le nom 'get_utilisateurs'
    # et la description de la docstring
    return jsonify({"message": "Liste des utilisateurs"})

@api_bp.route('/roles/custom', methods=['GET'])
@api_fonction(nom_fonction='get_all_roles', app_id=1, 
description="Récupère tous les rôles", auto_register=True)
def get_roles_custom():
    # Cette fonction sera enregistrée avec le nom 'get_all_roles'
    return jsonify({"message": "Liste des rôles"})


Exemple d'utilisation du décorateur auto_set_user_fields:

@app_bp.route('/ressource', methods=['POST'])
@jwt_required()  # Toujours mettre jwt_required en premier
@api_fonction(nom_fonction='create_ressource', app_id=1, description='Créer une nouvelle ressource', auto_register=True)
@trace_action(action_type="RESSOURCE", code_prefix="RES")
@auto_set_user_fields()  # Ce décorateur doit être placé après jwt_required
def create_ressource():
    # Les champs creer_par et modifier_par sont automatiquement ajoutés à request.json
    ressource_data = request.json
    
    # Utiliser les données normalement
    nouvelle_ressource = ressource_controller.create_ressource(ressource_data)
    
    return jsonify({
        'error': False,
        'message': {
            'fr': 'Ressource créée avec succès',
            'en': 'Resource created successfully'
        },
        'data': ressource_schema.dump(nouvelle_ressource)
    }), 201

@app_bp.route('/ressource/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_ressource', app_id=1, description='Mettre à jour une ressource', auto_register=True)
@trace_action(action_type="RESSOURCE", code_prefix="RES")
@auto_set_user_fields()
def update_ressource(id):
    # Le champ modifier_par est automatiquement ajouté à request.json
    ressource_data = request.json
    
    # Utiliser les données normalement
    ressource_updated = ressource_controller.update_ressource(id, ressource_data)
    
    return jsonify({
        'error': False,
        'message': {
            'fr': 'Ressource mise à jour avec succès',
            'en': 'Resource updated successfully'
        },
        'data': ressource_schema.dump(ressource_updated)
    })
"""
