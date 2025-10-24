from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.objectif_controller import ObjectifController
from app.common.schemas import ObjectifSchema
from datetime import datetime
from app.common.decorators import api_fonction, trace_action
from app.common.decorators import auto_set_user_fields

objectif_bp = Blueprint('objectif', __name__)
objectif_controller = ObjectifController()
objectif_schema = ObjectifSchema()
objectifs_schema = ObjectifSchema(many=True)

@objectif_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_objectifs', app_id=1, description='Récupérer tous les objectifs avec pagination', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
def get_objectifs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    objectifs, total_pages, total_items = objectif_controller.get_all_objectifs_paginated(page, per_page)
    
    response = {
        "error": False,
        "message": {
            "en": "Objectives retrieved successfully",
            "fr": "Objectifs récupérés avec succès"
        },
        "data": objectifs_schema.dump(objectifs),
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

@objectif_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_objectif', app_id=1, description='Récupérer un objectif par son ID', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
def get_objectif(id):
    objectif = objectif_controller.get_objectif_by_id(id)
    if not objectif:
        response = {
            "error": True,
            "message": {
                "en": "Objective not found",
                "fr": "Objectif non trouvé"
            }
        }
        return jsonify(response), 404
    
    response = {
        "error": False,
        "message": {
            "en": "Objective retrieved successfully",
            "fr": "Objectif récupéré avec succès"
        },
        "data": objectif_schema.dump(objectif)
    }
    return jsonify(response)

@objectif_bp.route('/utilisateur/<int:utilisateur_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_objectifs_by_utilisateur', app_id=1, description='Récupérer les objectifs d\'un utilisateur', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ_USR")
def get_objectifs_by_utilisateur(utilisateur_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    objectifs, total_pages, total_items = objectif_controller.get_objectifs_by_utilisateur_paginated(utilisateur_id, page, per_page)
    
    response = {
        "error": False,
        "message": {
            "en": "User objectives retrieved successfully",
            "fr": "Objectifs de l'utilisateur récupérés avec succès"
        },
        "data": objectifs_schema.dump(objectifs),
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

@objectif_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_objectif', app_id=1, description='Créer un nouvel objectif', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
@auto_set_user_fields()
def create_objectif():
    data = request.get_json()
    
    try:
        # Création de l'objectif
        objectif_data = {
            'id_utilisateur': data.get('id_utilisateur'),
            'type': data.get('type'),
            'description': data.get('description'),
            'periode': data.get('periode'),
            'titre': data.get('titre'),
            'statut': data.get('statut', 'En cours'),
            'progression': data.get('progression', 0.0),
            'creer_par': data.get('creer_par'),
            'modifier_par': data.get('modifier_par')
        }
        
        # Conversion des dates
        if 'date_debut' in data:
            objectif_data['date_debut'] = datetime.fromisoformat(data['date_debut'].replace('Z', '+00:00'))
        if 'date_fin' in data:
            objectif_data['date_fin'] = datetime.fromisoformat(data['date_fin'].replace('Z', '+00:00'))
        
        # Ajout du champ valeur s'il est présent
        if 'valeur' in data:
            objectif_data['valeur'] = data['valeur']
        
        objectif = objectif_controller.create_objectif(objectif_data)
        
        response = {
            "error": False,
            "message": {
                "en": "Objective created successfully",
                "fr": "Objectif créé avec succès"
            },
            "data": objectif_schema.dump(objectif)
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            "error": True,
            "message": {
                "en": "Failed to create objective",
                "fr": "Échec de la création de l'objectif"
            },
            "details": str(e)
        }
        return jsonify(response), 500

@objectif_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_objectif', app_id=1, description='Mettre à jour un objectif', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
@auto_set_user_fields()
def update_objectif(id):
    data = request.get_json()
    
    # Mise à jour de l'objectif
    objectif_data = {}
    
    if 'id_utilisateur' in data:
        objectif_data['id_utilisateur'] = data['id_utilisateur']
    if 'type' in data:
        objectif_data['type'] = data['type']
    if 'description' in data:
        objectif_data['description'] = data['description']
    if 'periode' in data:
        objectif_data['periode'] = data['periode']
    if 'valeur' in data:
        objectif_data['valeur'] = data['valeur']
    if 'titre' in data:
        objectif_data['titre'] = data['titre']
    if 'date_debut' in data:
        objectif_data['date_debut'] = datetime.fromisoformat(data['date_debut'].replace('Z', '+00:00'))
    if 'date_fin' in data:
        objectif_data['date_fin'] = datetime.fromisoformat(data['date_fin'].replace('Z', '+00:00'))
    if 'statut' in data:
        objectif_data['statut'] = data['statut']
    if 'progression' in data:
        objectif_data['progression'] = data['progression']
    if 'modifier_par' in data:
        objectif_data['modifier_par'] = data['modifier_par']
    
    objectif = objectif_controller.update_objectif(id, objectif_data)
    
    if not objectif:
        response = {
            "error": True,
            "message": {
                "en": "Objective not found",
                "fr": "Objectif non trouvé"
            }
        }
        return jsonify(response), 404
    
    response = {
        "error": False,
        "message": {
            "en": "Objective updated successfully",
            "fr": "Objectif mis à jour avec succès"
        },
        "data": objectif_schema.dump(objectif)
    }
    return jsonify(response)

@objectif_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_objectif', app_id=1, description='Supprimer un objectif', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ")
def delete_objectif(id):
    result = objectif_controller.delete_objectif(id)
    
    if not result:
        response = {
            "error": True,
            "message": {
                "en": "Objective not found",
                "fr": "Objectif non trouvé"
            }
        }
        return jsonify(response), 404
    
    response = {
        "error": False,
        "message": {
            "en": "Objective deleted successfully",
            "fr": "Objectif supprimé avec succès"
        }
    }
    return jsonify(response)

@objectif_bp.route('/type/<string:type_objectif>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_objectifs_by_type', app_id=1, description='Récupérer les objectifs par type', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ_TYPE")
def get_objectifs_by_type(type_objectif):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    objectifs, total_pages, total_items = objectif_controller.get_objectifs_by_type_paginated(type_objectif, page, per_page)
    
    response = {
        "error": False,
        "message": {
            "en": "Objectives by type retrieved successfully",
            "fr": "Objectifs par type récupérés avec succès"
        },
        "data": objectifs_schema.dump(objectifs),
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

@objectif_bp.route('/periode/<string:periode>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_objectifs_by_periode', app_id=1, description='Récupérer les objectifs par période', auto_register=True)
@trace_action(action_type="OBJECTIF", code_prefix="OBJ_PER")
def get_objectifs_by_periode(periode):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    objectifs, total_pages, total_items = objectif_controller.get_objectifs_by_periode_paginated(periode, page, per_page)
    
    response = {
        "error": False,
        "message": {
            "en": "Objectives by period retrieved successfully",
            "fr": "Objectifs par période récupérés avec succès"
        },
        "data": objectifs_schema.dump(objectifs),
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