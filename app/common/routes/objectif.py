from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.controllers.objectif_controller import ObjectifController
from app.common.schemas import ObjectifSchema
from app.common.decorators import api_fonction, trace_action, auto_set_user_fields

objectif_bp = Blueprint('objectif', __name__)
objectif_controller = ObjectifController()
objectif_schema = ObjectifSchema()
objectifs_schema = ObjectifSchema(many=True)

@objectif_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_objectifs', app_id=1, description='Récupérer les objectifs avec pagination', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
def get_objectifs():
    # Récupérer l'utilisateur courant
    from app.common.models import Utilisateur
    current_user_login = get_jwt_identity()
    current_user = Utilisateur.query.filter_by(login=current_user_login).first()
    if not current_user:
        return jsonify({
            "error": True,
            "message": {
                "en": "User not found",
                "fr": "Utilisateur non trouvé"
            }
        }), 404
    current_user_id = current_user.id_utilisateur
    
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 1000 pour l'export, 50 pour l'affichage normal
    max_per_page = 1000 if per_page > 100 else 50
    if per_page > max_per_page:
        per_page = max_per_page
    
    # Récupérer les objectifs selon les permissions de l'utilisateur
    objectifs, total_pages, total_items = objectif_controller.get_objectifs_for_user(current_user_id, page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Objectives retrieved successfully",
            "fr": "Objectifs récupérés avec succès"
        },
        "data": objectifs_schema.dump(objectifs),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@objectif_bp.route('/users', methods=['GET'])
@jwt_required()
#@api_fonction(nom_fonction='get_available_users', app_id=1, description='Récupérer les utilisateurs disponibles pour assignation d\'objectifs', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ_USERS")
def get_available_users():
    # Récupérer l'utilisateur courant
    from app.common.models import Utilisateur
    current_user_login = get_jwt_identity()
    current_user = Utilisateur.query.filter_by(login=current_user_login).first()
    if not current_user:
        return jsonify({
            "error": True,
            "message": {
                "en": "User not found",
                "fr": "Utilisateur non trouvé"
            }
        }), 404
    current_user_id = current_user.id_utilisateur
    
    # Récupérer les utilisateurs selon les permissions
    users = objectif_controller.get_available_users_for_objectif(current_user_id)
    
    from app.common.schemas import UtilisateurSchema
    users_schema = UtilisateurSchema(many=True)
    
    result = {
        "error": False,
        "message": {
            "en": "Available users retrieved successfully",
            "fr": "Utilisateurs disponibles récupérés avec succès"
        },
        "data": users_schema.dump(users)
    }
    return jsonify(result)

@objectif_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_objectif', app_id=1, description='Récupérer un objectif par son ID', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
def get_objectif(id):
    objectif = objectif_controller.get_objectif_by_id(id)
    if not objectif:
        result = {
            "error": True,
            "message": {
                "en": "Objective not found",
                "fr": "Objectif non trouvé"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Objective retrieved successfully",
            "fr": "Objectif récupéré avec succès"
        },
        "data": objectif_schema.dump(objectif)
    }
    return jsonify(result)

@objectif_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_objectif', app_id=1, description='Créer un nouvel objectif', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
@auto_set_user_fields()
def create_objectif():
    data = request.get_json()
    
    # Récupérer l'utilisateur courant
    from app.common.models import Utilisateur
    current_user_login = get_jwt_identity()
    current_user = Utilisateur.query.filter_by(login=current_user_login).first()
    if not current_user:
        return jsonify({
            "error": True,
            "message": {
                "en": "User not found",
                "fr": "Utilisateur non trouvé"
            }
        }), 404
    current_user_id = current_user.id_utilisateur
    
    try:
        objectif = objectif_controller.create_objectif(data, current_user_id)
        result = {
            "error": False,
            "message": {
                "en": "Objective created successfully",
                "fr": "Objectif créé avec succès"
            },
            "data": objectif_schema.dump(objectif)
        }
        return jsonify(result), 201
    
    except ValueError as e:
        # L'exception contient un dictionnaire avec les messages en FR et EN
        error_messages = e.args[0] if e.args and isinstance(e.args[0], dict) else {
            "fr": "Erreur lors de la création de l'objectif",
            "en": "Error creating objective"
        }
        
        result = {
            "error": True,
            "message": error_messages
        }
        return jsonify(result), 400
    
    except Exception as e:
        result = {
            "error": True,
            "message": {
                "en": "Failed to create objective",
                "fr": "Échec de la création de l'objectif"
            },
            "details": str(e)
        }
        return jsonify(result), 500

@objectif_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_objectif', app_id=1, description='Mettre à jour un objectif', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
@auto_set_user_fields()
def update_objectif(id):
    data = request.get_json()
    
    # Récupérer l'utilisateur courant
    from app.common.models import Utilisateur
    current_user_login = get_jwt_identity()
    current_user = Utilisateur.query.filter_by(login=current_user_login).first()
    if not current_user:
        return jsonify({
            "error": True,
            "message": {
                "en": "User not found",
                "fr": "Utilisateur non trouvé"
            }
        }), 404
    current_user_id = current_user.id_utilisateur
    
    try:
        objectif = objectif_controller.update_objectif(id, data, current_user_id)
        
        if not objectif:
            result = {
                "error": True,
                "message": {
                    "en": "Objective not found",
                    "fr": "Objectif non trouvé"
                }
            }
            return jsonify(result), 404
        
        result = {
            "error": False,
            "message": {
                "en": "Objective updated successfully",
                "fr": "Objectif mis à jour avec succès"
            },
            "data": objectif_schema.dump(objectif)
        }
        return jsonify(result)
    
    except ValueError as e:
        # L'exception contient un dictionnaire avec les messages en FR et EN
        error_messages = e.args[0] if e.args and isinstance(e.args[0], dict) else {
            "fr": "Erreur lors de la mise à jour de l'objectif",
            "en": "Error updating objective"
        }
        
        result = {
            "error": True,
            "message": error_messages
        }
        return jsonify(result), 400
    
    except Exception as e:
        result = {
            "error": True,
            "message": {
                "en": "Failed to update objective",
                "fr": "Échec de la mise à jour de l'objectif"
            },
            "details": str(e)
        }
        return jsonify(result), 500

@objectif_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_objectif', app_id=1, description='Supprimer un objectif', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
def delete_objectif(id):
    try:
        result_delete = objectif_controller.delete_objectif(id)
        
        if not result_delete:
            result = {
                "error": True,
                "message": {
                    "en": "Objective not found",
                    "fr": "Objectif non trouvé"
                }
            }
            return jsonify(result), 404
        
        result = {
            "error": False,
            "message": {
                "en": "Objective deleted successfully",
                "fr": "Objectif supprimé avec succès"
            }
        }
        return jsonify(result), 200
    
    except Exception as e:
        result = {
            "error": True,
            "message": {
                "en": "Failed to delete objective",
                "fr": "Échec de la suppression de l'objectif"
            },
            "details": str(e)
        }
        return jsonify(result), 500

@objectif_bp.route('/utilisateur/<int:utilisateur_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_objectifs_by_utilisateur', app_id=1, description='Récupérer les objectifs d\'un utilisateur', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ_USER")
def get_objectifs_by_utilisateur(utilisateur_id):
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 1000 pour l'export, 50 pour l'affichage normal
    max_per_page = 1000 if per_page > 100 else 50
    if per_page > max_per_page:
        per_page = max_per_page
    
    # Récupérer les objectifs paginés
    objectifs, total_pages, total_items = objectif_controller.get_objectifs_by_utilisateur_paginated(utilisateur_id, page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "User objectives retrieved successfully",
            "fr": "Objectifs de l'utilisateur récupérés avec succès"
        },
        "data": objectifs_schema.dump(objectifs),
        "pagination": pagination_metadata
    }
    return jsonify(result)