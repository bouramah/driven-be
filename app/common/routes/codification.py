from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.codification_controller import CodificationController
from app.common.schemas import CodificationSchema
from app.common.decorators import api_fonction
from app.common.decorators import trace_action
from app.common.decorators import auto_set_user_fields

codification_bp = Blueprint('codification', __name__)
codification_controller = CodificationController()
codification_schema = CodificationSchema()
codifications_schema = CodificationSchema(many=True)

@codification_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_codifications', app_id=1, description='Récupérer toutes les codifications avec pagination', auto_register=True)
@trace_action(action_type="CODIFICATION", code_prefix="COD")
def get_codifications():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50
    if per_page > 50:
        per_page = 50
    
    codifications, total_pages, total_items = codification_controller.get_all_codifications_paginated(page, per_page)
    
    response = {
        "error": False,
        "message": {
            "en": "Codifications retrieved successfully",
            "fr": "Codifications récupérées avec succès"
        },
        "data": codifications_schema.dump(codifications),
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None
        }
    }
    
    return jsonify(response)

@codification_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_codification', app_id=1, description='Récupérer une codification par son ID', auto_register=True)
@trace_action(action_type="CODIFICATION", code_prefix="COD")
def get_codification(id):
    codification = codification_controller.get_codification_by_id(id)
    if not codification:
        response = {
            "error": True,
            "message": {
                "en": "Codification not found",
                "fr": "Codification non trouvée"
            }
        }
        return jsonify(response), 404
    
    response = {
        "error": False,
        "message": {
            "en": "Codification retrieved successfully",
            "fr": "Codification récupérée avec succès"
        },
        "data": codification_schema.dump(codification)
    }
    return jsonify(response)

@codification_bp.route('/param/<string:param>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_codification_by_param', app_id=1, description='Récupérer une codification par son paramètre', auto_register=True)
@trace_action(action_type="CODIFICATION", code_prefix="COD_PARAM")
def get_codification_by_param(param):
    codification = codification_controller.get_codification_by_param(param)
    if not codification:
        response = {
            "error": True,
            "message": {
                "en": "Codification not found",
                "fr": "Codification non trouvée"
            }
        }
        return jsonify(response), 404
    
    response = {
        "error": False,
        "message": {
            "en": "Codification retrieved successfully",
            "fr": "Codification récupérée avec succès"
        },
        "data": codification_schema.dump(codification)
    }
    return jsonify(response)

@codification_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_codification', app_id=1, description='Créer une nouvelle codification', auto_register=True)
@trace_action(action_type="CODIFICATION", code_prefix="COD")
@auto_set_user_fields()
def create_codification():
    try:
        data = request.get_json()
        codification = codification_controller.create_codification(data)
        response = {
            "error": False,
            "message": {
                "en": "Codification created successfully",
                "fr": "Codification créée avec succès"
            },
            "data": codification_schema.dump(codification)
        }
        return jsonify(response), 201
    except ValueError as e:
        response = {
            "error": True,
            "message": {
                "en": str(e),
                "fr": str(e)
            }
        }
        return jsonify(response), 400
    except Exception as e:
        response = {
            "error": True,
            "message": {
                "en": "Failed to create codification",
                "fr": "Échec de la création de la codification"
            },
            "details": str(e)
        }
        return jsonify(response), 500

@codification_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_codification', app_id=1, description='Mettre à jour une codification', auto_register=True)
@trace_action(action_type="CODIFICATION", code_prefix="COD")
@auto_set_user_fields()
def update_codification(id):
    try:
        data = request.get_json()
        codification = codification_controller.update_codification(id, data)
        
        if not codification:
            response = {
                "error": True,
                "message": {
                    "en": "Codification not found",
                    "fr": "Codification non trouvée"
                }
            }
            return jsonify(response), 404
        
        response = {
            "error": False,
            "message": {
                "en": "Codification updated successfully",
                "fr": "Codification mise à jour avec succès"
            },
            "data": codification_schema.dump(codification)
        }
        return jsonify(response)
    except ValueError as e:
        response = {
            "error": True,
            "message": {
                "en": str(e),
                "fr": str(e)
            }
        }
        return jsonify(response), 400
    except Exception as e:
        response = {
            "error": True,
            "message": {
                "en": "Failed to update codification",
                "fr": "Échec de la mise à jour de la codification"
            },
            "details": str(e)
        }
        return jsonify(response), 500

@codification_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_codification', app_id=1, description='Supprimer une codification', auto_register=True)
@trace_action(action_type="CODIFICATION", code_prefix="COD")
def delete_codification(id):
    try:
        result = codification_controller.delete_codification(id)
        
        if not result:
            response = {
                "error": True,
                "message": {
                    "en": "Codification not found",
                    "fr": "Codification non trouvée"
                }
            }
            return jsonify(response), 404
        
        response = {
            "error": False,
            "message": {
                "en": "Codification deleted successfully",
                "fr": "Codification supprimée avec succès"
            }
        }
        return jsonify(response), 200
    
    except ValueError as e:
        # L'exception contient un dictionnaire avec les messages en FR et EN
        error_messages = e.args[0] if e.args and isinstance(e.args[0], dict) else {
            "fr": "Erreur lors de la suppression de la codification",
            "en": "Error deleting codification"
        }
        
        response = {
            "error": True,
            "message": error_messages
        }
        
        # Log pour debug
        print(f"DEBUG - Sending error response: {response}")
        
        return jsonify(response), 400
    
    except Exception as e:
        response = {
            "error": True,
            "message": {
                "en": "Failed to delete codification",
                "fr": "Échec de la suppression de la codification"
            },
            "details": str(e)
        }
        return jsonify(response), 500

@codification_bp.route('/search', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='search_codifications', app_id=1, description='Rechercher des codifications', auto_register=True)
@trace_action(action_type="CODIFICATION", code_prefix="COD_SEARCH")
def search_codifications():
    search_term = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50
    if per_page > 50:
        per_page = 50
    
    codifications, total_pages, total_items = codification_controller.search_codifications_paginated(search_term, page, per_page)
    
    response = {
        "error": False,
        "message": {
            "en": "Search results retrieved successfully",
            "fr": "Résultats de recherche récupérés avec succès"
        },
        "data": codifications_schema.dump(codifications),
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None
        }
    }
    return jsonify(response) 