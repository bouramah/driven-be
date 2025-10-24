from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.permission_page_controller import PermissionPageController
from app.common.schemas import PermissionPageSchema
from app.common.decorators import api_fonction
from app.common.decorators import trace_action, auto_set_user_fields

permission_page_bp = Blueprint('permission_page', __name__)
permission_page_controller = PermissionPageController()
permission_page_schema = PermissionPageSchema()
permission_pages_schema = PermissionPageSchema(many=True)

@permission_page_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_permission_pages', app_id=1, description='Récupérer toutes les associations permission-page', auto_register=True)
def get_permission_pages():
    permission_pages = permission_page_controller.get_all_permission_pages()
    return jsonify(permission_pages_schema.dump(permission_pages))

@permission_page_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_permission_page', app_id=1, description='Récupérer une association permission-page par son ID', auto_register=True)
def get_permission_page(id):
    permission_page = permission_page_controller.get_permission_page_by_id(id)
    if not permission_page:
        return jsonify({'message': 'Permission page not found'}), 404
    return jsonify(permission_page_schema.dump(permission_page))

@permission_page_bp.route('/page/<int:page_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_permission_pages_by_page', app_id=1, description='Récupérer les associations permission-page par ID de page', auto_register=True)
def get_permission_pages_by_page(page_id):
    permission_pages = permission_page_controller.get_permission_pages_by_page(page_id)
    return jsonify(permission_pages_schema.dump(permission_pages))

@permission_page_bp.route('/permission/<int:permission_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_permission_pages_by_permission', app_id=1, description='Récupérer les associations permission-page par ID de permission', auto_register=True)
def get_permission_pages_by_permission(permission_id):
    permission_pages = permission_page_controller.get_permission_pages_by_permission(permission_id)
    return jsonify(permission_pages_schema.dump(permission_pages))

@permission_page_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_permission_page', app_id=1, description='Créer une nouvelle association permission-page', auto_register=True)
@trace_action(action_type="PERMISSION_PAGE", code_prefix="PP")
@auto_set_user_fields()
def create_permission_page():
    data = request.get_json()
    permission_page = permission_page_controller.create_permission_page(data)
    return jsonify(permission_page_schema.dump(permission_page)), 201

@permission_page_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_permission_page', app_id=1, description='Mettre à jour une association permission-page', auto_register=True)
@trace_action(action_type="PERMISSION_PAGE", code_prefix="PP")
@auto_set_user_fields()
def update_permission_page(id):
    data = request.get_json()
    permission_page = permission_page_controller.update_permission_page(id, data)
    if not permission_page:
        return jsonify({'message': 'Permission page not found'}), 404
    return jsonify(permission_page_schema.dump(permission_page))

@permission_page_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_permission_page', app_id=1, description='Supprimer une association permission-page', auto_register=True)
def delete_permission_page(id):
    result = permission_page_controller.delete_permission_page(id)
    if not result:
        return jsonify({'message': 'Permission page not found'}), 404
    return '', 204 