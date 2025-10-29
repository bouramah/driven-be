from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.trace_controller import TraceController
from app.common.schemas import TraceSchema
from datetime import datetime
from app.common.decorators import api_fonction, trace_action
from app.common.decorators import auto_set_user_fields

trace_bp = Blueprint('trace', __name__)
trace_controller = TraceController()
trace_schema = TraceSchema()
traces_schema = TraceSchema(many=True)

@trace_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_traces', app_id=1, description='Récupérer toutes les traces avec pagination', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC")
def get_traces():
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 1000 pour l'export, 50 pour l'affichage normal
    max_per_page = 1000 if per_page > 100 else 50
    if per_page > max_per_page:
        per_page = max_per_page
    
    # Récupérer les entrées paginées
    traces_paginated = trace_controller.get_traces_paginated(page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": traces_paginated.total,
        "total_pages": traces_paginated.pages,
        "has_next": traces_paginated.has_next,
        "has_prev": traces_paginated.has_prev,
        "next_page": traces_paginated.next_num if traces_paginated.has_next else None,
        "prev_page": traces_paginated.prev_num if traces_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Trace entries retrieved successfully",
            "fr": "Entrées de trace récupérées avec succès"
        },
        "data": traces_schema.dump(traces_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@trace_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_trace', app_id=1, description='Récupérer une trace par son ID', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC")
def get_trace(id):
    trace = trace_controller.get_trace_by_id(id)
    if not trace:
        result = {
            "error": True,
            "message": {
                "en": "Trace entry not found",
                "fr": "Entrée de trace non trouvée"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Trace entry retrieved successfully",
            "fr": "Entrée de trace récupérée avec succès"
        },
        "data": trace_schema.dump(trace)
    }
    return jsonify(result)

@trace_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_trace', app_id=1, description='Créer une nouvelle trace', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC")
@auto_set_user_fields()
def create_trace():
    data = request.get_json()
    
    # Ajout automatique de la date si non fournie
    if 'date' not in data:
        data['date'] = datetime.utcnow()
    
    try:
        trace = trace_controller.create_trace(data)
        result = {
            "error": False,
            "message": {
                "en": "Trace entry created successfully",
                "fr": "Entrée de trace créée avec succès"
            },
            "data": trace_schema.dump(trace)
        }
        return jsonify(result), 201
    except Exception as e:
        result = {
            "error": True,
            "message": {
                "en": "Failed to create trace entry",
                "fr": "Échec de la création de l'entrée de trace"
            },
            "details": str(e)
        }
        return jsonify(result), 500

@trace_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_trace', app_id=1, description='Mettre à jour une trace', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC")
@auto_set_user_fields()
def update_trace(id):
    data = request.get_json()
    trace = trace_controller.update_trace(id, data)
    
    if not trace:
        result = {
            "error": True,
            "message": {
                "en": "Trace entry not found",
                "fr": "Entrée de trace non trouvée"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Trace entry updated successfully",
            "fr": "Entrée de trace mise à jour avec succès"
        },
        "data": trace_schema.dump(trace)
    }
    return jsonify(result)

@trace_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_trace', app_id=1, description='Supprimer une trace', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC")
def delete_trace(id):
    success = trace_controller.delete_trace(id)
    if not success:
        result = {
            "error": True,
            "message": {
                "en": "Trace entry not found",
                "fr": "Entrée de trace non trouvée"
            }
        }
        return jsonify(result), 404
    
    result = {
        "error": False,
        "message": {
            "en": "Trace entry deleted successfully",
            "fr": "Entrée de trace supprimée avec succès"
        }
    }
    return jsonify(result)

@trace_bp.route('/utilisateur/<int:utilisateur_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_traces_by_utilisateur', app_id=1, description='Récupérer les traces d\'un utilisateur', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC_USR")
def get_traces_by_utilisateur(utilisateur_id):
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 1000 pour l'export, 50 pour l'affichage normal
    max_per_page = 1000 if per_page > 100 else 50
    if per_page > max_per_page:
        per_page = max_per_page
    
    # Récupérer les entrées paginées
    traces_paginated = trace_controller.get_traces_by_utilisateur_paginated(utilisateur_id, page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": traces_paginated.total,
        "total_pages": traces_paginated.pages,
        "has_next": traces_paginated.has_next,
        "has_prev": traces_paginated.has_prev,
        "next_page": traces_paginated.next_num if traces_paginated.has_next else None,
        "prev_page": traces_paginated.prev_num if traces_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Trace entries retrieved successfully",
            "fr": "Entrées de trace récupérées avec succès"
        },
        "data": traces_schema.dump(traces_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@trace_bp.route('/action/<string:action>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_traces_by_action', app_id=1, description='Récupérer les traces par action', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC_ACT")
def get_traces_by_action(action):
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 1000 pour l'export, 50 pour l'affichage normal
    max_per_page = 1000 if per_page > 100 else 50
    if per_page > max_per_page:
        per_page = max_per_page
    
    # Récupérer les entrées paginées
    traces_paginated = trace_controller.get_traces_by_action_paginated(action, page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": traces_paginated.total,
        "total_pages": traces_paginated.pages,
        "has_next": traces_paginated.has_next,
        "has_prev": traces_paginated.has_prev,
        "next_page": traces_paginated.next_num if traces_paginated.has_next else None,
        "prev_page": traces_paginated.prev_num if traces_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Trace entries retrieved successfully",
            "fr": "Entrées de trace récupérées avec succès"
        },
        "data": traces_schema.dump(traces_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@trace_bp.route('/date-range', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_traces_by_date_range', app_id=1, description='Récupérer les traces par plage de dates', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC_DATE")
def get_traces_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        result = {
            "error": True,
            "message": {
                "en": "Start date and end date are required",
                "fr": "Les dates de début et de fin sont requises"
            }
        }
        return jsonify(result), 400
        
    try:
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)
    except ValueError:
        result = {
            "error": True,
            "message": {
                "en": "Invalid date format. Use ISO format (YYYY-MM-DD)",
                "fr": "Format de date invalide. Utilisez le format ISO (AAAA-MM-JJ)"
            }
        }
        return jsonify(result), 400
    
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 1000 pour l'export, 50 pour l'affichage normal
    max_per_page = 1000 if per_page > 100 else 50
    if per_page > max_per_page:
        per_page = max_per_page
    
    # Récupérer les entrées paginées
    traces_paginated = trace_controller.get_traces_by_date_range_paginated(start_date, end_date, page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": traces_paginated.total,
        "total_pages": traces_paginated.pages,
        "has_next": traces_paginated.has_next,
        "has_prev": traces_paginated.has_prev,
        "next_page": traces_paginated.next_num if traces_paginated.has_next else None,
        "prev_page": traces_paginated.prev_num if traces_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Trace entries retrieved successfully",
            "fr": "Entrées de trace récupérées avec succès"
        },
        "data": traces_schema.dump(traces_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@trace_bp.route('/search', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='search_traces', app_id=1, description='Rechercher des traces', auto_register=True)
@trace_action(action_type="TRACE", code_prefix="TRC_SEARCH")
def search_traces():
    try:
        search_term = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if per_page > 50:
            per_page = 50
        
        if not search_term:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Search term is required',
                    'fr': 'Le terme de recherche est requis'
                }
            }), 400
        
        traces_paginated = trace_controller.search_traces_paginated(search_term, page, per_page)
        
        pagination_metadata = {
            "page": page,
            "per_page": per_page,
            "total_items": traces_paginated.total,
            "total_pages": traces_paginated.pages,
            "has_next": traces_paginated.has_next,
            "has_prev": traces_paginated.has_prev,
            "next_page": traces_paginated.next_num if traces_paginated.has_next else None,
            "prev_page": traces_paginated.prev_num if traces_paginated.has_prev else None
        }
        
        result = {
            "error": False,
            "message": {
                "en": "Search results retrieved successfully",
                "fr": "Résultats de recherche récupérés avec succès"
            },
            "data": traces_schema.dump(traces_paginated.items),
            "pagination": pagination_metadata
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while searching traces',
                'fr': 'Erreur lors de la recherche des traces'
            },
            'details': str(e)
        }), 500 