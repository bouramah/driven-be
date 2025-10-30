from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.settings_controller import SettingsController
from app.common.schemas import SettingsSchema
from app.common.decorators import api_fonction, trace_action
from app.common.decorators import auto_set_user_fields

settings_bp = Blueprint('settings', __name__)
settings_controller = SettingsController()
setting_schema = SettingsSchema()
settings_schema = SettingsSchema(many=True)

@settings_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_settings', app_id=1, description='Récupérer tous les paramètres avec pagination', auto_register=True)
@trace_action(action_type="SETTINGS", code_prefix="SET")
def get_settings():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50
    if per_page > 50:
        per_page = 50
    
    settings, total_pages, total_items = settings_controller.get_all_settings_paginated(page, per_page)
    
    response = {
        "error": False,
        "message": {
            "en": "Settings retrieved successfully",
            "fr": "Paramètres récupérés avec succès"
        },
        "data": settings_schema.dump(settings),
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

@settings_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_setting', app_id=1, description='Récupérer un paramètre par son ID', auto_register=True)
@trace_action(action_type="SETTINGS", code_prefix="SET")
def get_setting(id):
    setting = settings_controller.get_setting_by_id(id)
    if not setting:
        response = {
            "error": True,
            "message": {
                "en": "Setting not found",
                "fr": "Paramètre non trouvé"
            }
        }
        return jsonify(response), 404
    
    response = {
        "error": False,
        "message": {
            "en": "Setting retrieved successfully",
            "fr": "Paramètre récupéré avec succès"
        },
        "data": setting_schema.dump(setting)
    }
    return jsonify(response)

# Route supprimée - on utilise maintenant get_setting_by_user_and_codification

@settings_bp.route('/utilisateur/<int:utilisateur_id>', methods=['GET'])
@jwt_required()
@trace_action(action_type="SETTINGS", code_prefix="SET_USR")
def get_settings_by_utilisateur(utilisateur_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50
    if per_page > 50:
        per_page = 50
    
    settings, total_pages, total_items = settings_controller.get_settings_by_utilisateur_paginated(utilisateur_id, page, per_page)
    
    response = {
        "error": False,
        "message": {
            "en": "User settings retrieved successfully",
            "fr": "Paramètres de l'utilisateur récupérés avec succès"
        },
        "data": settings_schema.dump(settings),
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

@settings_bp.route('/', methods=['POST'])
@jwt_required()
#@api_fonction(nom_fonction='create_setting', app_id=1, description='Créer un nouveau paramètre', auto_register=True)
@trace_action(action_type="SETTINGS", code_prefix="SET")
@auto_set_user_fields()
def create_setting():
    data = request.get_json()
    
    try:
        setting = settings_controller.create_setting(data)
        response = {
            "error": False,
            "message": {
                "en": "Setting created successfully",
                "fr": "Paramètre créé avec succès"
            },
            "data": setting_schema.dump(setting)
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            "error": True,
            "message": {
                "en": "Failed to create setting",
                "fr": "Échec de la création du paramètre"
            },
            "details": str(e)
        }
        return jsonify(response), 500

@settings_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
#@api_fonction(nom_fonction='update_setting', app_id=1, description='Mettre à jour un paramètre', auto_register=True)
@trace_action(action_type="SETTINGS", code_prefix="SET")
@auto_set_user_fields()
def update_setting(id):
    data = request.get_json()
    setting = settings_controller.update_setting(id, data)
    
    if not setting:
        response = {
            "error": True,
            "message": {
                "en": "Setting not found",
                "fr": "Paramètre non trouvé"
            }
        }
        return jsonify(response), 404
    
    response = {
        "error": False,
        "message": {
            "en": "Setting updated successfully",
            "fr": "Paramètre mis à jour avec succès"
        },
        "data": setting_schema.dump(setting)
    }
    return jsonify(response)

@settings_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_setting', app_id=1, description='Supprimer un paramètre', auto_register=True)
@trace_action(action_type="SETTINGS", code_prefix="SET")
def delete_setting(id):
    result = settings_controller.delete_setting(id)
    
    if not result:
        response = {
            "error": True,
            "message": {
                "en": "Setting not found",
                "fr": "Paramètre non trouvé"
            }
        }
        return jsonify(response), 404
    
    response = {
        "error": False,
        "message": {
            "en": "Setting deleted successfully",
            "fr": "Paramètre supprimé avec succès"
        }
    }
    return jsonify(response)
