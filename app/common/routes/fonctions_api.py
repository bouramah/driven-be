from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.common.controllers.fonction_api_controller import FonctionAPIController
from app.common.schemas import FonctionAPISchema, PermissionSchema
from app.common.decorators import api_fonction
from app.common.decorators import trace_action
from app.common.decorators import auto_set_user_fields

# Création du blueprint
fonction_api_bp = Blueprint('fonction_api', __name__)

# Initialisation des schémas
fonction_api_schema = FonctionAPISchema()
fonctions_api_schema = FonctionAPISchema(many=True)
permissions_schema = PermissionSchema(many=True)

# Initialisation du contrôleur
fonctions_api_controller = FonctionAPIController()

@fonction_api_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_fonctions', app_id=1, description='Récupérer toutes les fonctions API avec pagination', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI")
def get_fonctions():
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    try:
        # Récupérer les fonctions API paginées
        fonctions_paginated = fonctions_api_controller.get_fonctions_paginated(page, per_page)
        
        # Préparer les métadonnées de pagination
        pagination_metadata = {
            "page": page,
            "per_page": per_page,
            "total_items": fonctions_paginated.total,
            "total_pages": fonctions_paginated.pages,
            "has_next": fonctions_paginated.has_next,
            "has_prev": fonctions_paginated.has_prev,
            "next_page": fonctions_paginated.next_num if fonctions_paginated.has_next else None,
            "prev_page": fonctions_paginated.prev_num if fonctions_paginated.has_prev else None
        }
        
        result = {
            "error": False,
            "message": {
                "en": "Functions retrieved successfully",
                "fr": "Fonctions récupérées avec succès"
            },
            "data": fonctions_api_schema.dump(fonctions_paginated.items),
            "pagination": pagination_metadata
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving functions',
                'fr': 'Erreur lors de la récupération des fonctions'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/application/<int:app_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_fonctions_by_app', app_id=1, description='Récupérer les fonctions API par application', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI_APP")
def get_fonctions_by_app(app_id):
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    try:
        # Récupérer les fonctions API paginées pour une application
        fonctions_paginated = fonctions_api_controller.get_fonctions_by_app_paginated(app_id, page, per_page)
        
        # Préparer les métadonnées de pagination
        pagination_metadata = {
            "page": page,
            "per_page": per_page,
            "total_items": fonctions_paginated.total,
            "total_pages": fonctions_paginated.pages,
            "has_next": fonctions_paginated.has_next,
            "has_prev": fonctions_paginated.has_prev,
            "next_page": fonctions_paginated.next_num if fonctions_paginated.has_next else None,
            "prev_page": fonctions_paginated.prev_num if fonctions_paginated.has_prev else None
        }
        
        result = {
            "error": False,
            "message": {
                "en": "Functions retrieved successfully",
                "fr": "Fonctions récupérées avec succès"
            },
            "data": fonctions_api_schema.dump(fonctions_paginated.items),
            "pagination": pagination_metadata
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving functions',
                'fr': 'Erreur lors de la récupération des fonctions'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_fonction', app_id=1, description='Récupérer une fonction API par son ID', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI")
def get_fonction(id):
    try:
        # Récupérer la fonction API par son ID
        fonction = fonctions_api_controller.get_fonction_by_id(id)
        
        if not fonction:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Function not found',
                    'fr': 'Fonction non trouvée'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Function retrieved successfully',
                'fr': 'Fonction récupérée avec succès'
            },
            'data': fonction_api_schema.dump(fonction)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving function',
                'fr': 'Erreur lors de la récupération de la fonction'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_fonction', app_id=1, description='Créer une nouvelle fonction API', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI")
@auto_set_user_fields()
def create_fonction():
    try:
        # Récupérer les données de la requête
        fonction_data = request.json
        
        # Créer la nouvelle fonction API
        nouvelle_fonction = fonctions_api_controller.create_fonction(fonction_data)
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Function created successfully',
                'fr': 'Fonction créée avec succès'
            },
            'data': fonction_api_schema.dump(nouvelle_fonction)
        }), 201
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while creating function',
                'fr': 'Erreur lors de la création de la fonction'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_fonction', app_id=1, description='Mettre à jour une fonction API', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI")
@auto_set_user_fields()
def update_fonction(id):
    try:
        # Récupérer les données de la requête
        fonction_data = request.json
        
        # Mettre à jour la fonction API
        fonction = fonctions_api_controller.update_fonction(id, fonction_data)
        
        if not fonction:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Function not found',
                    'fr': 'Fonction non trouvée'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Function updated successfully',
                'fr': 'Fonction mise à jour avec succès'
            },
            'data': fonction_api_schema.dump(fonction)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while updating function',
                'fr': 'Erreur lors de la mise à jour de la fonction'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_fonction', app_id=1, description='Supprimer une fonction API', auto_register=True)
def delete_fonction(id):
    try:
        # Supprimer la fonction API
        result = fonctions_api_controller.delete_fonction(id)
        
        if not result:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Function not found',
                    'fr': 'Fonction non trouvée'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Function deleted successfully',
                'fr': 'Fonction supprimée avec succès'
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while deleting function',
                'fr': 'Erreur lors de la suppression de la fonction'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/<int:id>/permissions', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_fonction_permissions', app_id=1, description='Récupérer les permissions d\'une fonction API', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI_PERM")
def get_fonction_permissions(id):
    try:
        # Récupérer les permissions de la fonction API
        permissions = fonctions_api_controller.get_fonction_permissions(id)
        
        if permissions is None:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Function not found',
                    'fr': 'Fonction non trouvée'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permissions retrieved successfully',
                'fr': 'Permissions récupérées avec succès'
            },
            'data': permissions_schema.dump(permissions)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving permissions',
                'fr': 'Erreur lors de la récupération des permissions'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/<int:id>/permissions', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='assign_permissions', app_id=1, description='Assigner des permissions à une fonction API', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI_PERM")
@auto_set_user_fields()
def assign_permissions(id):
    try:
        # Récupérer les données de la requête
        permission_data = request.json
        permission_ids = permission_data.get('permission_ids', [])
        
        # Assigner les permissions à la fonction API
        fonction = fonctions_api_controller.assign_permissions(id, permission_ids)
        
        if not fonction:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Function not found',
                    'fr': 'Fonction non trouvée'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permissions assigned successfully',
                'fr': 'Permissions assignées avec succès'
            },
            'data': fonction_api_schema.dump(fonction)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while assigning permissions',
                'fr': 'Erreur lors de l\'assignation des permissions'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/<int:id>/permissions', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='remove_permissions', app_id=1, description='Supprimer des permissions d\'une fonction API', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI_PERM")
def remove_permissions(id):
    try:
        # Récupérer les données de la requête
        permission_data = request.json
        permission_ids = permission_data.get('permission_ids', [])
        
        # Retirer les permissions de la fonction API
        fonction = fonctions_api_controller.remove_permissions(id, permission_ids)
        
        if not fonction:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Function not found',
                    'fr': 'Fonction non trouvée'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permissions removed successfully',
                'fr': 'Permissions retirées avec succès'
            },
            'data': fonction_api_schema.dump(fonction)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while removing permissions',
                'fr': 'Erreur lors du retrait des permissions'
            },
            'details': str(e)
        }), 500

@fonction_api_bp.route('/<int:fonction_id>/permissions/<int:permission_id>', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='assign_permission', app_id=1, description='Assigner une permission spécifique à une fonction API', auto_register=True)
@trace_action(action_type="FONCTION_API", code_prefix="FAPI_PERM")
@auto_set_user_fields()
def assign_permission(fonction_id, permission_id):
    try:
        # Assigner une permission spécifique à la fonction API
        fonction = fonctions_api_controller.assign_permissions(fonction_id, [permission_id])
        
        if not fonction:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Function not found',
                    'fr': 'Fonction non trouvée'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permission assigned successfully',
                'fr': 'Permission assignée avec succès'
            },
            'data': fonction_api_schema.dump(fonction)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while assigning permission',
                'fr': 'Erreur lors de l\'assignation de la permission'
            },
            'details': str(e)
        }), 500 