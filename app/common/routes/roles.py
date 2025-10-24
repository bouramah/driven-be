from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.role_controller import RoleController
from app.common.schemas import RoleSchema, PermissionSchema, RolePermissionSchema
from app.common.decorators import api_fonction, trace_action
from app.common.decorators import auto_set_user_fields

role_bp = Blueprint('roles', __name__)
roles_controller = RoleController()
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
permissions_schema = PermissionSchema(many=True)
role_permissions_schema = RolePermissionSchema(many=True)

@role_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_roles', app_id=1, description='Récupérer tous les rôles avec leurs permissions', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE")
def get_roles():
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    # Récupérer les entrées paginées
    roles_paginated = roles_controller.get_roles_paginated(page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": roles_paginated.total,
        "total_pages": roles_paginated.pages,
        "has_next": roles_paginated.has_next,
        "has_prev": roles_paginated.has_prev,
        "next_page": roles_paginated.next_num if roles_paginated.has_next else None,
        "prev_page": roles_paginated.prev_num if roles_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Roles with permissions retrieved successfully",
            "fr": "Rôles avec permissions récupérés avec succès"
        },
        "data": roles_schema.dump(roles_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@role_bp.route('/application/<int:app_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_roles_by_app', app_id=1, description='Récupérer les rôles par application', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE_APP")
def get_roles_by_app(app_id):
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    # Récupérer les entrées paginées
    roles_paginated = roles_controller.get_roles_by_app_paginated(app_id, page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": roles_paginated.total,
        "total_pages": roles_paginated.pages,
        "has_next": roles_paginated.has_next,
        "has_prev": roles_paginated.has_prev,
    }
    
    # Sérialiser les données
    result = roles_schema.dump(roles_paginated.items)
    
    return jsonify({
        "error": False,
        "message": {
            "fr": "Rôles récupérés avec succès",
            "en": "Roles retrieved successfully"
        },
        "data": {
            "items": result,
            "pagination": pagination_metadata
        }
    }), 200

@role_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_role', app_id=1, description='Récupérer un rôle par son ID', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE")
def get_role(id):
    try:
        role = roles_controller.get_role_by_id(id)
        if not role:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Role not found',
                    'fr': 'Rôle non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Role retrieved successfully',
                'fr': 'Rôle récupéré avec succès'
            },
            'data': role_schema.dump(role)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving role',
                'fr': 'Erreur lors de la récupération du rôle'
            },
            'details': str(e)
        }), 500

@role_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_role', app_id=1, description='Créer un nouveau rôle', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE")
@auto_set_user_fields()
def create_role():
    try:
        data = request.json
        role = roles_controller.create_role(data)
        return jsonify({
            'error': False,
            'message': {
                'en': 'Role created successfully',
                'fr': 'Rôle créé avec succès'
            },
            'data': role_schema.dump(role)
        }), 201
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while creating role',
                'fr': 'Erreur lors de la création du rôle'
            },
            'details': str(e)
        }), 500

@role_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_role', app_id=1, description='Mettre à jour un rôle', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE")
@auto_set_user_fields()
def update_role(id):
    try:
        data = request.json
        role = roles_controller.update_role(id, data)
        if not role:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Role not found',
                    'fr': 'Rôle non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Role updated successfully',
                'fr': 'Rôle mis à jour avec succès'
            },
            'data': role_schema.dump(role)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while updating role',
                'fr': 'Erreur lors de la mise à jour du rôle'
            },
            'details': str(e)
        }), 500

@role_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_role', app_id=1, description='Supprimer un rôle', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE")
def delete_role(id):
    try:
        result = roles_controller.delete_role(id)
        if result is None:  # Le rôle a des permissions associées
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Cannot delete role because it has associated permissions',
                    'fr': 'Impossible de supprimer le rôle car il a des permissions associées'
                }
            }), 400
        elif not result:  # Le rôle n'existe pas
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Role not found',
                    'fr': 'Rôle non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Role deleted successfully',
                'fr': 'Rôle supprimé avec succès'
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while deleting role',
                'fr': 'Erreur lors de la suppression du rôle'
            },
            'details': str(e)
        }), 500

@role_bp.route('/<int:id>/permissions', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_role_permissions', app_id=1, description='Récupérer les permissions d\'un rôle', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE_PERM")
def get_role_permissions(id):
    try:
        permissions = roles_controller.get_role_permissions(id)
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permissions retrieved successfully',
                'fr': 'Permissions récupérées avec succès'
            },
            'data': permissions_schema.dump(permissions)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving permissions',
                'fr': 'Erreur lors de la récupération des permissions'
            },
            'details': str(e)
        }), 500

@role_bp.route('/<int:id>/permissions', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='assign_permissions', app_id=1, description='Assigner des permissions à un rôle', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE_PERM")
@auto_set_user_fields()
def assign_permissions(id):
    try:
        data = request.json
        permission_ids = data.get('permission_ids', [])
        role = roles_controller.assign_permissions(id, permission_ids)
        if not role:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Role not found',
                    'fr': 'Rôle non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permissions assigned successfully',
                'fr': 'Permissions affectées avec succès'
            },
            'data': role_schema.dump(role)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while assigning permissions',
                'fr': 'Erreur lors de l\'affectation des permissions'
            },
            'details': str(e)
        }), 500

@role_bp.route('/<int:id>/permissions', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='remove_permissions', app_id=1, description='Supprimer des permissions d\'un rôle', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE_PERM")
def remove_permissions(id):
    try:
        data = request.json
        permission_ids = data.get('permission_ids', [])
        role = roles_controller.remove_permissions(id, permission_ids)
        if not role:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Role not found',
                    'fr': 'Rôle non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permissions removed successfully',
                'fr': 'Permissions retirées avec succès'
            },
            'data': role_schema.dump(role)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while removing permissions',
                'fr': 'Erreur lors du retrait des permissions'
            },
            'details': str(e)
        }), 500

@role_bp.route('/<int:role_id>/permissions/<int:permission_id>', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='assign_permission', app_id=1, description='Assigner une permission spécifique à un rôle', auto_register=True)
@trace_action(action_type="ROLE", code_prefix="ROLE_PERM")
@auto_set_user_fields()
def assign_permission(role_id, permission_id):
    try:
        role = roles_controller.assign_permissions(role_id, [permission_id])
        if not role:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Role not found',
                    'fr': 'Rôle non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Permission assigned successfully',
                'fr': 'Permission affectée avec succès'
            },
            'data': role_schema.dump(role)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while assigning permission',
                'fr': 'Erreur lors de l\'affectation de la permission'
            },
            'details': str(e)
        }), 500