from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.permission_controller import PermissionController
from app.common.schemas import PermissionSchema, RoleSchema
from app.common.decorators import api_fonction, trace_action
from app.common.decorators import auto_set_user_fields


permission_bp = Blueprint('permissions', __name__)
permissions_controller = PermissionController()
permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)
roles_schema = RoleSchema(many=True)

@permission_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_permissions', app_id=1, description='Récupérer toutes les permissions avec pagination', auto_register=True)
@trace_action(action_type="PERMISSION", code_prefix="PERM")
def get_permissions():
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    # Récupérer les entrées paginées
    permissions_paginated = permissions_controller.get_permissions_paginated(page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": permissions_paginated.total,
        "total_pages": permissions_paginated.pages,
        "has_next": permissions_paginated.has_next,
        "has_prev": permissions_paginated.has_prev,
        "next_page": permissions_paginated.next_num if permissions_paginated.has_next else None,
        "prev_page": permissions_paginated.prev_num if permissions_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Permissions retrieved successfully",
            "fr": "Permissions récupérées avec succès"
        },
        "data": permissions_schema.dump(permissions_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@permission_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_permission', app_id=1, description='Récupérer une permission par son ID', auto_register=True)
@trace_action(action_type="PERMISSION", code_prefix="PERM")
def get_permission(id):
    try:
        permission = permissions_controller.get_permission_by_id(id)
        if not permission:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Permission not found',
                    'fr': 'Permission non trouvée'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permission retrieved successfully',
                'fr': 'Permission récupérée avec succès'
            },
            'data': permission_schema.dump(permission)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving permission',
                'fr': 'Erreur lors de la récupération de la permission'
            },
            'details': str(e)
        }), 500

@permission_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_permission', app_id=1, description='Créer une nouvelle permission', auto_register=True)
@trace_action(action_type="PERMISSION", code_prefix="PERM")
@auto_set_user_fields()
def create_permission():
    try:
        data = request.json
        permission = permissions_controller.create_permission(data)
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permission created successfully',
                'fr': 'Permission créée avec succès'
            },
            'data': permission_schema.dump(permission)
        }), 201
    except ValueError as e:
        return jsonify({
            'error': True,
            'message': {
                'en': str(e),
                'fr': str(e)
            }
        }), 400
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while creating permission',
                'fr': 'Erreur lors de la création de la permission'
            },
            'details': str(e)
        }), 500

@permission_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_permission', app_id=1, description='Mettre à jour une permission', auto_register=True)
@trace_action(action_type="PERMISSION", code_prefix="PERM")
@auto_set_user_fields()
def update_permission(id):
    try:
        data = request.json
        permission = permissions_controller.update_permission(id, data)
        if not permission:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Permission not found',
                    'fr': 'Permission non trouvée'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permission updated successfully',
                'fr': 'Permission mise à jour avec succès'
            },
            'data': permission_schema.dump(permission)
        })
    except ValueError as e:
        return jsonify({
            'error': True,
            'message': {
                'en': str(e),
                'fr': str(e)
            }
        }), 400
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while updating permission',
                'fr': 'Erreur lors de la mise à jour de la permission'
            },
            'details': str(e)
        }), 500

@permission_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_permission', app_id=1, description='Supprimer une permission', auto_register=True)
@trace_action(action_type="PERMISSION", code_prefix="PERM")
def delete_permission(id):
    try:
        result = permissions_controller.delete_permission(id)
        if not result:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Permission not found',
                    'fr': 'Permission non trouvée'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permission deleted successfully',
                'fr': 'Permission supprimée avec succès'
            }
        })
    except ValueError as e:
        error_messages = e.args[0] if e.args and isinstance(e.args[0], dict) else {
            'fr': "Impossible de supprimer la permission",
            'en': 'Unable to delete permission'
        }
        return jsonify({
            'error': True,
            'message': error_messages
        }), 400
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while deleting permission',
                'fr': 'Erreur lors de la suppression de la permission'
            },
            'details': str(e)
        }), 500

@permission_bp.route('/<int:id>/roles', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_roles_with_permission', app_id=1, description='Récupérer les rôles ayant une permission spécifique', auto_register=True)
@trace_action(action_type="PERMISSION", code_prefix="PERM_ROLE")
def get_roles_with_permission(id):
    try:
        roles = permissions_controller.get_roles_with_permission(id)
        return jsonify({
            'error': False,
            'message': {
                'en': 'Roles retrieved successfully',
                'fr': 'Rôles récupérés avec succès'
            },
            'data': roles_schema.dump(roles)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving roles',
                'fr': 'Erreur lors de la récupération des rôles'
            },
            'details': str(e)
        }), 500