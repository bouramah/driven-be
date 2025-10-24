from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.blacklist_controller import BlackListController
from app.common.schemas import BlackListSchema
from datetime import datetime
from app.common.decorators import api_fonction
from app.common.decorators import trace_action
from app.common.decorators import auto_set_user_fields

blacklist_bp = Blueprint('blacklist', __name__)
blacklist_controller = BlackListController()
blacklist_schema = BlackListSchema()
blacklists_schema = BlackListSchema(many=True)

@blacklist_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_blacklists', app_id=1, description='Récupérer toutes les entrées de la liste noire avec pagination', auto_register=True)
@trace_action(action_type="BLACKLIST", code_prefix="BL")
def get_blacklists():
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    # Récupérer les entrées paginées
    blacklists_paginated = blacklist_controller.get_all_blacklists_paginated(page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": blacklists_paginated.total,
        "total_pages": blacklists_paginated.pages,
        "has_next": blacklists_paginated.has_next,
        "has_prev": blacklists_paginated.has_prev,
        "next_page": blacklists_paginated.next_num if blacklists_paginated.has_next else None,
        "prev_page": blacklists_paginated.prev_num if blacklists_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Blacklist entries retrieved successfully",
            "fr": "Entrées de la liste noire récupérées avec succès"
        },
        "data": blacklists_schema.dump(blacklists_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@blacklist_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_blacklist', app_id=1, description='Récupérer une entrée de la liste noire par son ID', auto_register=True)
@trace_action(action_type="BLACKLIST", code_prefix="BL")
def get_blacklist(id):
    blacklist = blacklist_controller.get_blacklist_by_id(id)
    if not blacklist:
        result = {
            "error": True,
            "message": {
                "en": "Blacklist entry not found",
                "fr": "Entrée de la liste noire non trouvée"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Blacklist entry retrieved successfully",
            "fr": "Entrée de la liste noire récupérée avec succès"
        },
        "data": blacklist_schema.dump(blacklist)
    }
    return jsonify(result)

@blacklist_bp.route('/number/<string:number>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_blacklist_by_number', app_id=1, description='Récupérer une entrée de la liste noire par son numéro', auto_register=True)
@trace_action(action_type="BLACKLIST", code_prefix="BL_NUMBER")
def get_blacklist_by_number(number):
    blacklist = blacklist_controller.get_blacklist_by_number(number)
    if not blacklist:
        result = {
            "error": True,
            "message": {
                "en": "Number not found in blacklist",
                "fr": "Numéro non trouvé dans la liste noire"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Blacklist entry retrieved successfully",
            "fr": "Entrée de la liste noire récupérée avec succès"
        },
        "data": blacklist_schema.dump(blacklist)
    }
    return jsonify(result)

@blacklist_bp.route('/check/<string:number>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='is_number_blacklisted', app_id=1, description='Vérifier si un numéro est dans la liste noire', auto_register=True)
@trace_action(action_type="BLACKLIST", code_prefix="BL_CHECK")
def is_number_blacklisted(number):
    is_blacklisted = blacklist_controller.is_number_blacklisted(number)
    result = {
        "error": False,
        "message": {
            "en": "Number check completed",
            "fr": "Vérification du numéro terminée"
        },
        "data": {
            "is_blacklisted": is_blacklisted
        }
    }
    return jsonify(result)

@blacklist_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_blacklist', app_id=1, description='Créer une nouvelle entrée dans la liste noire', auto_register=True)
@trace_action(action_type="BLACKLIST", code_prefix="BL")
@auto_set_user_fields()
def create_blacklist():
    try:
        # Récupérer les données de la requête
        blacklist_data = request.json
        
        # Créer la nouvelle entrée dans la liste noire
        nouvelle_blacklist = blacklist_controller.create_blacklist(blacklist_data)
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Blacklist entry created successfully',
                'fr': 'Entrée de la liste noire créée avec succès'
            },
            'data': blacklist_schema.dump(nouvelle_blacklist)
        }), 201
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while creating blacklist entry',
                'fr': 'Erreur lors de la création de l\'entrée dans la liste noire'
            },
            'details': str(e)
        }), 500

@blacklist_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_blacklist', app_id=1, description='Supprimer une entrée de la liste noire', auto_register=True)
@trace_action(action_type="BLACKLIST", code_prefix="BL")
def delete_blacklist(id):
    success = blacklist_controller.delete_blacklist(id)
    if not success:
        result = {
            "error": True,
            "message": {
                "en": "Blacklist entry not found",
                "fr": "Entrée de la liste noire non trouvée"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Blacklist entry deleted successfully",
            "fr": "Entrée de la liste noire supprimée avec succès"
        }
    }
    return jsonify(result)

@blacklist_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_blacklist', app_id=1, description='Mettre à jour une entrée de la liste noire', auto_register=True)
@trace_action(action_type="BLACKLIST", code_prefix="BL")
@auto_set_user_fields()
def update_blacklist(id):
    try:
        # Récupérer les données de la requête
        blacklist_data = request.json
        
        # Mettre à jour l'entrée dans la liste noire
        blacklist_updated = blacklist_controller.update_blacklist(id, blacklist_data)
        
        if not blacklist_updated:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Blacklist entry not found',
                    'fr': 'Entrée de la liste noire non trouvée'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Blacklist entry updated successfully',
                'fr': 'Entrée de la liste noire mise à jour avec succès'
            },
            'data': blacklist_schema.dump(blacklist_updated)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while updating blacklist entry',
                'fr': 'Erreur lors de la mise à jour de l\'entrée dans la liste noire'
            },
            'details': str(e)
        }), 500

