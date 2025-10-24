from flask import Blueprint, request, jsonify
from app.common.services.objectif_service import ObjectifService
from app.common.schemas import ObjectifSchema
from app.common.utils.auth import token_required
from app.common.utils.validation import validate_request_data

objectif_bp = Blueprint('objectif', __name__)
objectif_service = ObjectifService()
objectif_schema = ObjectifSchema()
objectifs_schema = ObjectifSchema(many=True)

@objectif_bp.route('/objectifs', methods=['GET'])
def get_all_objectifs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    objectifs, total_pages, total_items = objectif_service.get_all_objectifs_paginated(page, per_page)
    result = objectifs_schema.dump(objectifs)
    
    return jsonify({
        'data': result,
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_items': total_items
        }
    }), 200

@objectif_bp.route('/objectifs/<int:objectif_id>', methods=['GET'])
def get_objectif_by_id(objectif_id):
    objectif = objectif_service.get_objectif_by_id(objectif_id)
    
    if not objectif:
        return jsonify({'message': 'Objectif non trouvé'}), 404
        
    result = objectif_schema.dump(objectif)
    return jsonify({'data': result}), 200

@objectif_bp.route('/utilisateurs/<int:utilisateur_id>/objectifs', methods=['GET'])
def get_objectifs_by_utilisateur(utilisateur_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    objectifs, total_pages, total_items = objectif_service.get_objectifs_by_utilisateur_paginated(utilisateur_id, page, per_page)
    result = objectifs_schema.dump(objectifs)
    
    return jsonify({
        'data': result,
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_items': total_items
        }
    }), 200

@objectif_bp.route('/objectifs/type/<string:type_objectif>', methods=['GET'])
def get_objectifs_by_type(type_objectif):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    objectifs, total_pages, total_items = objectif_service.get_objectifs_by_type_paginated(type_objectif, page, per_page)
    result = objectifs_schema.dump(objectifs)
    
    return jsonify({
        'data': result,
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_items': total_items
        }
    }), 200

@objectif_bp.route('/objectifs/periode/<string:periode>', methods=['GET'])
def get_objectifs_by_periode(periode):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    objectifs, total_pages, total_items = objectif_service.get_objectifs_by_periode_paginated(periode, page, per_page)
    result = objectifs_schema.dump(objectifs)
    
    return jsonify({
        'data': result,
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_items': total_items
        }
    }), 200

@objectif_bp.route('/objectifs', methods=['POST'])
@token_required
def create_objectif(current_user):
    data = request.get_json()
    
    # Validation des données
    required_fields = ['id_utilisateur', 'type', 'description', 'periode']
    validation_result = validate_request_data(data, required_fields)
    
    if validation_result:
        return validation_result
    
    # Création de l'objectif
    objectif_data = {
        'id_utilisateur': data['id_utilisateur'],
        'type': data['type'],
        'description': data['description'],
        'periode': data['periode']
    }
    
    # Ajout du champ valeur s'il est présent
    if 'valeur' in data:
        objectif_data['valeur'] = data['valeur']
    
    objectif = objectif_service.create_objectif(objectif_data)
    result = objectif_schema.dump(objectif)
    
    return jsonify({'message': 'Objectif créé avec succès', 'data': result}), 201

@objectif_bp.route('/objectifs/<int:objectif_id>', methods=['PUT'])
@token_required
def update_objectif(current_user, objectif_id):
    objectif = objectif_service.get_objectif_by_id(objectif_id)
    
    if not objectif:
        return jsonify({'message': 'Objectif non trouvé'}), 404
        
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
    
    updated_objectif = objectif_service.update_objectif(objectif_id, objectif_data)
    result = objectif_schema.dump(updated_objectif)
    
    return jsonify({'message': 'Objectif mis à jour avec succès', 'data': result}), 200

@objectif_bp.route('/objectifs/<int:objectif_id>', methods=['DELETE'])
@token_required
def delete_objectif(current_user, objectif_id):
    result = objectif_service.delete_objectif(objectif_id)
    
    if not result:
        return jsonify({'message': 'Objectif non trouvé'}), 404
        
    return jsonify({'message': 'Objectif supprimé avec succès'}), 200 