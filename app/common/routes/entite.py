from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.entite_controller import EntiteController
from app.common.schemas import EntiteSchema
from app.common.decorators import api_fonction
from app.common.decorators import trace_action
from app.common.decorators import auto_set_user_fields

entite_bp = Blueprint('entite', __name__)
entite_controller = EntiteController()
entite_schema = EntiteSchema()
entites_schema = EntiteSchema(many=True)

@entite_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_entites', app_id=1, description='Récupérer toutes les entités avec pagination', auto_register=True)
@trace_action(action_type="ENTITE", code_prefix="ENT")
def get_entites():
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    # Récupérer les entrées paginées
    entites_paginated = entite_controller.get_entites_paginated(page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": entites_paginated.total,
        "total_pages": entites_paginated.pages,
        "has_next": entites_paginated.has_next,
        "has_prev": entites_paginated.has_prev,
        "next_page": entites_paginated.next_num if entites_paginated.has_next else None,
        "prev_page": entites_paginated.prev_num if entites_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Entities retrieved successfully",
            "fr": "Entités récupérées avec succès"
        },
        "data": entites_schema.dump(entites_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@entite_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_entite', app_id=1, description='Récupérer une entité par son ID', auto_register=True)
@trace_action(action_type="ENTITE", code_prefix="ENT")
def get_entite(id):
    entite = entite_controller.get_entite_by_id(id)
    if not entite:
        result = {
            "error": True,
            "message": {
                "en": "Entity not found",
                "fr": "Entité non trouvée"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Entity retrieved successfully",
            "fr": "Entité récupérée avec succès"
        },
        "data": entite_schema.dump(entite)
    }
    return jsonify(result)

@entite_bp.route('/code/<string:code>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_entite_by_code', app_id=1, description='Récupérer une entité par son code', auto_register=True)
@trace_action(action_type="ENTITE", code_prefix="ENT_CODE")
def get_entite_by_code(code):
    entite = entite_controller.get_entite_by_code(code)
    if not entite:
        result = {
            "error": True,
            "message": {
                "en": "Entity not found",
                "fr": "Entité non trouvée"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Entity retrieved successfully",
            "fr": "Entité récupérée avec succès"
        },
        "data": entite_schema.dump(entite)
    }
    return jsonify(result)

@entite_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_entite', app_id=1, description='Créer une nouvelle entité', auto_register=True)
@trace_action(action_type="ENTITE", code_prefix="ENT")
@auto_set_user_fields()
def create_entite():
    try:
        data = request.get_json()
        entite = entite_controller.create_entite(data)
        result = {
            "error": False,
            "message": {
                "en": "Entity created successfully",
                "fr": "Entité créée avec succès"
            },
            "data": entite_schema.dump(entite)
        }
        return jsonify(result), 201
    except ValueError as e:
        error_msg = str(e)
        if '|' in error_msg and ':' in error_msg:
            parts = error_msg.split('|')
            message = {
                "fr": parts[0].split(':', 1)[1] if 'fr:' in parts[0] else error_msg,
                "en": parts[1].split(':', 1)[1] if 'en:' in parts[1] else error_msg
            }
        else:
            message = {"fr": error_msg, "en": error_msg}
        
        result = {
            "error": True,
            "message": message
        }
        return jsonify(result), 400
    except Exception as e:
        result = {
            "error": True,
            "message": {
                "en": "Failed to create entity",
                "fr": "Échec de la création de l'entité"
            },
            "details": str(e)
        }
        return jsonify(result), 500

@entite_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_entite', app_id=1, description='Mettre à jour une entité', auto_register=True)
@trace_action(action_type="ENTITE", code_prefix="ENT")
@auto_set_user_fields()
def update_entite(id):
    try:
        data = request.get_json()
        entite = entite_controller.update_entite(id, data)
        
        if not entite:
            result = {
                "error": True,
                "message": {
                    "en": "Entity not found",
                    "fr": "Entité non trouvée"
                }
            }
            return jsonify(result), 404
        
        result = {
            "error": False,
            "message": {
                "en": "Entity updated successfully",
                "fr": "Entité mise à jour avec succès"
            },
            "data": entite_schema.dump(entite)
        }
        return jsonify(result)
    except ValueError as e:
        error_msg = str(e)
        # Parser le format bilingue "fr:message|en:message"
        if '|' in error_msg and ':' in error_msg:
            parts = error_msg.split('|')
            message = {
                "fr": parts[0].split(':', 1)[1] if 'fr:' in parts[0] else error_msg,
                "en": parts[1].split(':', 1)[1] if 'en:' in parts[1] else error_msg
            }
        else:
            message = {"fr": error_msg, "en": error_msg}
        
        result = {
            "error": True,
            "message": message
        }
        return jsonify(result), 400
    except Exception as e:
        result = {
            "error": True,
            "message": {
                "en": "Failed to update entity",
                "fr": "Échec de la mise à jour de l'entité"
            },
            "details": str(e)
        }
        return jsonify(result), 500

@entite_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_entite', app_id=1, description='Supprimer une entité', auto_register=True)
@trace_action(action_type="ENTITE", code_prefix="ENT")
def delete_entite(id):
    try:
        success = entite_controller.delete_entite(id)
        if not success:
            result = {
                "error": True,
                "message": {
                    "en": "Entity not found",
                    "fr": "Entité non trouvée"
                }
            }
            return jsonify(result), 404
        result = {
            "error": False,
            "message": {
                "en": "Entity deleted successfully",
                "fr": "Entité supprimée avec succès"
            }
        }
        return jsonify(result)
    except ValueError as e:
        error_messages = e.args[0] if e.args and isinstance(e.args[0], dict) else {
            "fr": "Impossible de supprimer l'entité",
            "en": "Unable to delete entity"
        }
        return jsonify({
            "error": True,
            "message": error_messages
        }), 400
    except Exception as e:
        return jsonify({
            "error": True,
            "message": {
                "en": "Error while deleting entity",
                "fr": "Erreur lors de la suppression de l'entité"
            },
            "details": str(e)
        }), 500