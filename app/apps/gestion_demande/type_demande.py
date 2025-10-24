from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.apps.gestion_demande.controllers.type_demande_controller import TypeDemandeController
from app.apps.gestion_demande.schemas import TypeDemandeSchema

type_demande_bp = Blueprint('type_demande', __name__)
type_demande_controller = TypeDemandeController()
type_demande_schema = TypeDemandeSchema()
types_demande_schema = TypeDemandeSchema(many=True)

@type_demande_bp.route('/', methods=['GET'])
@jwt_required()
def get_types_demande():
    types = type_demande_controller.get_all_types_demande()
    return jsonify(types_demande_schema.dump(types))

@type_demande_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_type_demande(id):
    type_demande = type_demande_controller.get_type_demande_by_id(id)
    if not type_demande:
        return jsonify({'message': 'Type de demande not found'}), 404
    return jsonify(type_demande_schema.dump(type_demande))

@type_demande_bp.route('/', methods=['POST'])
@jwt_required()
def create_type_demande():
    data = request.get_json()
    type_demande = type_demande_controller.create_type_demande(data)
    return jsonify(type_demande_schema.dump(type_demande)), 201

@type_demande_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_type_demande(id):
    data = request.get_json()
    type_demande = type_demande_controller.update_type_demande(id, data)
    if not type_demande:
        return jsonify({'message': 'Type de demande not found'}), 404
    return jsonify(type_demande_schema.dump(type_demande))

@type_demande_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_type_demande(id):
    result = type_demande_controller.delete_type_demande(id)
    if not result:
        return jsonify({'message': 'Type de demande not found'}), 404
    return '', 204 