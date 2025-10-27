from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.utilisateur_controller import UtilisateurController
from app.common.schemas import UtilisateurSchema, UtilisateurRoleSchema
from datetime import datetime
from app.common.decorators import trace_action, api_fonction
from app.common.decorators import auto_set_user_fields

utilisateur_bp = Blueprint('utilisateur', __name__)
utilisateur_controller = UtilisateurController()
utilisateur_schema = UtilisateurSchema()
utilisateurs_schema = UtilisateurSchema(many=True)
utilisateur_roles_schema = UtilisateurRoleSchema(many=True)

@utilisateur_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_utilisateurs', app_id=1, description='Récupérer la liste des utilisateurs avec pagination', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER")
def get_utilisateurs():
    """Récupérer la liste des utilisateurs avec pagination"""
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    # Récupérer les entrées paginées
    utilisateurs_paginated = utilisateur_controller.get_utilisateurs_paginated(page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": utilisateurs_paginated.total,
        "total_pages": utilisateurs_paginated.pages,
        "has_next": utilisateurs_paginated.has_next,
        "has_prev": utilisateurs_paginated.has_prev,
        "next_page": utilisateurs_paginated.next_num if utilisateurs_paginated.has_next else None,
        "prev_page": utilisateurs_paginated.prev_num if utilisateurs_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Users retrieved successfully",
            "fr": "Utilisateurs récupérés avec succès"
        },
        "data": utilisateurs_schema.dump(utilisateurs_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@utilisateur_bp.route('/entite/<int:entite_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_utilisateurs_by_entite', app_id=1, description='Récupérer les utilisateurs par entité', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_ENTITY")
def get_utilisateurs_by_entite(entite_id):
    """Récupérer la liste des utilisateurs d'une entité avec pagination"""
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    # Récupérer les entrées paginées
    utilisateurs_paginated = utilisateur_controller.get_utilisateurs_by_entite_paginated(entite_id, page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": utilisateurs_paginated.total,
        "total_pages": utilisateurs_paginated.pages,
        "has_next": utilisateurs_paginated.has_next,
        "has_prev": utilisateurs_paginated.has_prev,
        "next_page": utilisateurs_paginated.next_num if utilisateurs_paginated.has_next else None,
        "prev_page": utilisateurs_paginated.prev_num if utilisateurs_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Users retrieved successfully",
            "fr": "Utilisateurs récupérés avec succès"
        },
        "data": utilisateurs_schema.dump(utilisateurs_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@utilisateur_bp.route('/role/<int:role_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_utilisateurs_by_role', app_id=1, description='Récupérer les utilisateurs par rôle', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_ROLE")
def get_utilisateurs_by_role(role_id):
    """Récupérer la liste des utilisateurs ayant un rôle spécifique avec pagination"""
    # Récupérer les paramètres de pagination depuis la requête
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limiter per_page à un maximum de 50 pour éviter les requêtes trop lourdes
    if per_page > 50:
        per_page = 50
    
    # Récupérer les entrées paginées
    utilisateurs_paginated = utilisateur_controller.get_utilisateurs_by_role_paginated(role_id, page, per_page)
    
    # Préparer les métadonnées de pagination
    pagination_metadata = {
        "page": page,
        "per_page": per_page,
        "total_items": utilisateurs_paginated.total,
        "total_pages": utilisateurs_paginated.pages,
        "has_next": utilisateurs_paginated.has_next,
        "has_prev": utilisateurs_paginated.has_prev,
        "next_page": utilisateurs_paginated.next_num if utilisateurs_paginated.has_next else None,
        "prev_page": utilisateurs_paginated.prev_num if utilisateurs_paginated.has_prev else None
    }
    
    result = {
        "error": False,
        "message": {
            "en": "Users retrieved successfully",
            "fr": "Utilisateurs récupérés avec succès"
        },
        "data": utilisateurs_schema.dump(utilisateurs_paginated.items),
        "pagination": pagination_metadata
    }
    return jsonify(result)

@utilisateur_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_utilisateur', app_id=1, description='Récupérer un utilisateur par son ID', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER")
def get_utilisateur(id):
    """Récupérer un utilisateur par son ID"""
    try:
        utilisateur = utilisateur_controller.get_utilisateur_by_id(id)
        if not utilisateur:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'User not found',
                    'fr': 'Utilisateur non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'User retrieved successfully',
                'fr': 'Utilisateur récupéré avec succès'
            },
            'data': utilisateur_schema.dump(utilisateur)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving user',
                'fr': 'Erreur lors de la récupération de l\'utilisateur'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_utilisateur', app_id=1, description='Créer un nouvel utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER")
@auto_set_user_fields()
def create_utilisateur():
    """Créer un nouvel utilisateur"""
    try:
        data = request.json
        # Convertir la chaîne de date en objet datetime
        if 'date_expiration' in data and data['date_expiration'] is not None and data['date_expiration'] != "" and isinstance(data['date_expiration'], str):
            data['date_expiration'] = datetime.fromisoformat(data['date_expiration'].replace('T', ' '))
        utilisateur = utilisateur_controller.create_utilisateur(data)
        return jsonify({
            'error': False,
            'message': {
                'en': 'User created successfully',
                'fr': 'Utilisateur créé avec succès'
            },
            'data': utilisateur_schema.dump(utilisateur)
        }), 201
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while creating user',
                'fr': 'Erreur lors de la création de l\'utilisateur'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_utilisateur', app_id=1, description='Mettre à jour un utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER")
@auto_set_user_fields()
def update_utilisateur(id):
    """Mettre à jour un utilisateur"""
    try:
        data = request.json
        utilisateur = utilisateur_controller.update_utilisateur(id, data)
        if not utilisateur:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'User not found',
                    'fr': 'Utilisateur non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'User updated successfully',
                'fr': 'Utilisateur mis à jour avec succès'
            },
            'data': utilisateur_schema.dump(utilisateur)
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
                'en': 'Error while updating user',
                'fr': 'Erreur lors de la mise à jour de l\'utilisateur'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_utilisateur', app_id=1, description='Supprimer un utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER")
def delete_utilisateur(id):
    """Supprimer un utilisateur"""
    try:
        result = utilisateur_controller.delete_utilisateur(id)
        if not result:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'User not found',
                    'fr': 'Utilisateur non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'User deleted successfully',
                'fr': 'Utilisateur supprimé avec succès'
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while deleting user',
                'fr': 'Erreur lors de la suppression de l\'utilisateur'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:utilisateur_id>/prolonger', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='prolonger_utilisateur', app_id=1, description='Prolonger la durée de validité d\'un utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_EXPIRATION")
@auto_set_user_fields()
def prolonger_utilisateur(utilisateur_id):
    """Prolonger la date d'expiration d'un utilisateur"""
    try:
        data = request.json
        nouvelle_date_expiration = data.get('date_expiration')
        
        utilisateur = utilisateur_controller.prolonger_date_expiration(
            utilisateur_id, 
            nouvelle_date_expiration
        )
        
        if not utilisateur:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'User not found',
                    'fr': 'Utilisateur non trouvé'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Expiration date extended successfully',
                'fr': 'Date d\'expiration prolongée avec succès'
            },
            'data': utilisateur_schema.dump(utilisateur)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while extending expiration date',
                'fr': 'Erreur lors de la prolongation de la date d\'expiration'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:id>/profil', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_profil', app_id=1, description='Mettre à jour le profil d\'un utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_PROFILE")
@auto_set_user_fields()
def update_profil(id):
    """Mettre à jour le profil d'un utilisateur"""
    try:
        data = request.json
        utilisateur = utilisateur_controller.update_profil(id, data)
        if not utilisateur:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'User not found',
                    'fr': 'Utilisateur non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Profile updated successfully',
                'fr': 'Profil mis à jour avec succès'
            },
            'data': utilisateur_schema.dump(utilisateur)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while updating profile',
                'fr': 'Erreur lors de la mise à jour du profil'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:id>/statut', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_statut', app_id=1, description='Mettre à jour le statut d\'un utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_STATUS")
@auto_set_user_fields()
def update_statut(id):
    """Mettre à jour le statut d'un utilisateur"""
    try:
        data = request.json
        statut = data.get('statut')
        if not statut:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Status is required',
                    'fr': 'Le statut est requis'
                }
            }), 400
        
        utilisateur = utilisateur_controller.update_statut(id, statut)
        if not utilisateur:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'User not found',
                    'fr': 'Utilisateur non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Status updated successfully',
                'fr': 'Statut mis à jour avec succès'
            },
            'data': utilisateur_schema.dump(utilisateur)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while updating status',
                'fr': 'Erreur lors de la mise à jour du statut'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:id>/eligibilite', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='verifier_eligibilite', app_id=1, description='Vérifier l\'éligibilité d\'un utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_ELIGIBILITY")
def verifier_eligibilite(id):
    """Vérifier l'éligibilité d'un utilisateur"""
    try:
        app_id = request.args.get('app_id', type=int)
        resultat = utilisateur_controller.verifier_eligibilite(id, app_id)
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Eligibility checked successfully',
                'fr': 'Éligibilité vérifiée avec succès'
            },
            'data': resultat
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while checking eligibility',
                'fr': 'Erreur lors de la vérification de l\'éligibilité'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:id>/roles', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_utilisateur_roles', app_id=1, description='Récupérer les rôles d\'un utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_ROLES")
def get_utilisateur_roles(id):
    """Récupérer tous les rôles d'un utilisateur"""
    try:
        roles = utilisateur_controller.get_utilisateur_roles(id)
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'User roles retrieved successfully',
                'fr': 'Rôles de l\'utilisateur récupérés avec succès'
            },
            'data': utilisateur_roles_schema.dump(roles)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving user roles',
                'fr': 'Erreur lors de la récupération des rôles de l\'utilisateur'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:id>/roles', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='assign_role', app_id=1, description='Assigner un ou plusieurs rôles à un utilisateur', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_ROLES")
@auto_set_user_fields()
def assign_role(id):
    """Assigner un ou plusieurs rôles à un utilisateur"""
    try:
        data = request.json
        role_ids = data.get('role_ids')  # Liste des IDs de rôles
        creer_par = data.get('creer_par')
        modifier_par = data.get('modifier_par')
        
        if not all([role_ids, creer_par, modifier_par]):
            return jsonify({
                'error': True,
                'message': {
                    'en': 'role_ids (list), creer_par and modifier_par are required',
                    'fr': 'role_ids (liste), creer_par et modifier_par sont requis'
                }
            }), 400
            
        if not isinstance(role_ids, list):
            return jsonify({
                'error': True,
                'message': {
                    'en': 'role_ids must be a list of role IDs',
                    'fr': 'role_ids doit être une liste d\'identifiants de rôles'
                }
            }), 400
        
        utilisateur_roles = utilisateur_controller.assign_multiple_roles(id, role_ids, creer_par, modifier_par)
        
        return jsonify({
            'error': False,
            'message': {
                'en': f'{len(utilisateur_roles)} role(s) assigned successfully',
                'fr': f'{len(utilisateur_roles)} rôle(s) assigné(s) avec succès'
            },
            'data': utilisateur_roles_schema.dump(utilisateur_roles)
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
                'en': 'Error while assigning roles',
                'fr': 'Erreur lors de l\'assignation des rôles'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/<int:id>/roles/<int:role_id>/application/<int:app_id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='remove_role', app_id=1, description='Supprimer un rôle d\'un utilisateur pour une application spécifique', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_ROLES")
def remove_role(id, role_id, app_id):
    """Retirer un rôle à un utilisateur"""
    try:
        result = utilisateur_controller.remove_role(id, role_id, app_id)
        
        if not result:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Role not found for this user and application',
                    'fr': 'Rôle non trouvé pour cet utilisateur et cette application'
                }
            }), 404
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Role removed successfully',
                'fr': 'Rôle retiré avec succès'
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while removing role',
                'fr': 'Erreur lors du retrait du rôle'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/search', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='search_utilisateurs', app_id=1, description='Rechercher des utilisateurs', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_SEARCH")
def search_utilisateurs():
    """Rechercher des utilisateurs par nom, prénom, login ou email"""
    try:
        # Récupérer les paramètres de recherche
        query = request.args.get('q', '')
        if not query or len(query) < 3:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Search query must be at least 3 characters',
                    'fr': 'La requête de recherche doit comporter au moins 3 caractères'
                }
            }), 400
        
        # Récupérer les paramètres de pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Limiter per_page à un maximum de 50
        if per_page > 50:
            per_page = 50
        
        # Effectuer la recherche
        from app.common.models import Utilisateur
        from sqlalchemy import or_
        
        search_query = f"%{query}%"
        utilisateurs_paginated = Utilisateur.query.filter(
            or_(
                Utilisateur.nom.ilike(search_query),
                Utilisateur.prenom.ilike(search_query),
                Utilisateur.login.ilike(search_query),
                Utilisateur.email.ilike(search_query)
            )
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        # Préparer les métadonnées de pagination
        pagination_metadata = {
            "page": page,
            "per_page": per_page,
            "total_items": utilisateurs_paginated.total,
            "total_pages": utilisateurs_paginated.pages,
            "has_next": utilisateurs_paginated.has_next,
            "has_prev": utilisateurs_paginated.has_prev,
            "next_page": utilisateurs_paginated.next_num if utilisateurs_paginated.has_next else None,
            "prev_page": utilisateurs_paginated.prev_num if utilisateurs_paginated.has_prev else None
        }
        
        return jsonify({
            'error': False,
            'message': {
                'en': 'Search completed successfully',
                'fr': 'Recherche effectuée avec succès'
            },
            'data': utilisateurs_schema.dump(utilisateurs_paginated.items),
            'pagination': pagination_metadata
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while searching users',
                'fr': 'Erreur lors de la recherche d\'utilisateurs'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/login/<string:login>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_utilisateur_by_login', app_id=1, description='Récupérer un utilisateur par son login', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_LOGIN")
def get_utilisateur_by_login(login):
    """Récupérer un utilisateur par son login"""
    try:
        utilisateur = utilisateur_controller.get_utilisateur_by_login(login)
        if not utilisateur:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'User not found',
                    'fr': 'Utilisateur non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'User retrieved successfully',
                'fr': 'Utilisateur récupéré avec succès'
            },
            'data': utilisateur_schema.dump(utilisateur)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving user',
                'fr': 'Erreur lors de la récupération de l\'utilisateur'
            },
            'details': str(e)
        }), 500

@utilisateur_bp.route('/email/<string:email>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_utilisateur_by_email', app_id=1, description='Récupérer un utilisateur par son email', auto_register=True)
@trace_action(action_type="UTILISATEUR", code_prefix="USER_EMAIL")
def get_utilisateur_by_email(email):
    """Récupérer un utilisateur par son email"""
    try:
        utilisateur = utilisateur_controller.get_utilisateur_by_email(email)
        if not utilisateur:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'User not found',
                    'fr': 'Utilisateur non trouvé'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'User retrieved successfully',
                'fr': 'Utilisateur récupéré avec succès'
            },
            'data': utilisateur_schema.dump(utilisateur)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving user',
                'fr': 'Erreur lors de la récupération de l\'utilisateur'
            },
            'details': str(e)
        }), 500