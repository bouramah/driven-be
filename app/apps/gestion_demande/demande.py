from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.apps.gestion_demande.controllers.demande_controller import DemandeController
from app.apps.gestion_demande.schemas import DemandeSchema

demande_bp = Blueprint('demande', __name__)
demande_controller = DemandeController()
demande_schema = DemandeSchema()
demandes_schema = DemandeSchema(many=True)

@demande_bp.route('/', methods=['GET'])
@jwt_required()
def get_demandes():
    demandes = demande_controller.get_all_demandes()
    return jsonify(demandes_schema.dump(demandes))

@demande_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_demande(id):
    demande = demande_controller.get_demande_by_id(id)
    if not demande:
        return jsonify({'message': 'Demande not found'}), 404
    return jsonify(demande_schema.dump(demande))

@demande_bp.route('/numero/<string:numero>', methods=['GET'])
@jwt_required()
def get_demande_by_numero(numero):
    demande = demande_controller.get_demande_by_numero(numero)
    if not demande:
        return jsonify({'message': 'Demande not found'}), 404
    return jsonify(demande_schema.dump(demande))

@demande_bp.route('/', methods=['POST'])
@jwt_required()
def create_demande():
    data = request.get_json()
    demande = demande_controller.create_demande(data)
    return jsonify(demande_schema.dump(demande)), 201

@demande_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_demande(id):
    data = request.get_json()
    demande = demande_controller.update_demande(id, data)
    if not demande:
        return jsonify({'message': 'Demande not found'}), 404
    return jsonify(demande_schema.dump(demande))

@demande_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_demande(id):
    result = demande_controller.delete_demande(id)
    if not result:
        return jsonify({'message': 'Demande not found'}), 404
    return '', 204

@demande_bp.route('/statut/<string:statut>', methods=['GET'])
@jwt_required()
def get_demandes_by_statut(statut):
    demandes = demande_controller.get_demandes_by_statut(statut)
    return jsonify(demandes_schema.dump(demandes))

@demande_bp.route('/type/<int:type_id>', methods=['GET'])
@jwt_required()
def get_demandes_by_type(type_id):
    demandes = demande_controller.get_demandes_by_type(type_id)
    return jsonify(demandes_schema.dump(demandes))

@demande_bp.route('/utilisateur/<int:utilisateur_id>', methods=['GET'])
@jwt_required()
def get_demandes_by_utilisateur(utilisateur_id):
    demandes = demande_controller.get_demandes_by_utilisateur(utilisateur_id)
    return jsonify(demandes_schema.dump(demandes))

@demande_bp.route('/entite/<int:entite_id>', methods=['GET'])
@jwt_required()
def get_demandes_by_entite(entite_id):
    demandes = demande_controller.get_demandes_by_entite(entite_id)
    return jsonify(demandes_schema.dump(demandes))

@demande_bp.route('/priorite/<string:niveau_priorite>', methods=['GET'])
@jwt_required()
def get_demandes_by_priorite(niveau_priorite):
    demandes = demande_controller.get_demandes_by_priorite(niveau_priorite)
    return jsonify(demandes_schema.dump(demandes))

@demande_bp.route('/<int:id>/prendre-en-charge', methods=['POST'])
@jwt_required()
def prendre_en_charge_demande(id):
    utilisateur_id = get_jwt_identity()
    demande = demande_controller.prendre_en_charge_demande(id, utilisateur_id)
    if not demande:
        return jsonify({'message': 'Impossible de prendre en charge cette demande'}), 400
    return jsonify(demande_schema.dump(demande))

@demande_bp.route('/<int:id>/terminer', methods=['POST'])
@jwt_required()
def terminer_demande(id):
    demande = demande_controller.terminer_demande(id)
    if not demande:
        return jsonify({'message': 'Impossible de terminer cette demande'}), 400
    return jsonify(demande_schema.dump(demande))

@demande_bp.route('/search', methods=['GET'])
@jwt_required()
def search_demandes():
    search_term = request.args.get('q', '')
    demandes = demande_controller.search_demandes(search_term)
    return jsonify(demandes_schema.dump(demandes))
