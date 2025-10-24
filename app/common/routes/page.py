from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.page_controller import PageController
from app.common.schemas import PageSchema
from app.common.decorators import api_fonction, trace_action
from app.common.decorators import auto_set_user_fields

page_bp = Blueprint('page', __name__)
page_controller = PageController()
page_schema = PageSchema()
pages_schema = PageSchema(many=True)

@page_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_pages', app_id=1, description='Récupérer toutes les pages', auto_register=True)
@trace_action(action_type="PAGE", code_prefix="PAGE")
def get_pages():
    try:
        pages = page_controller.get_all_pages()
        return jsonify({
            'error': False,
            'message': {
                'en': 'Pages retrieved successfully',
                'fr': 'Pages récupérées avec succès'
            },
            'data': pages_schema.dump(pages)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving pages',
                'fr': 'Erreur lors de la récupération des pages'
            },
            'details': str(e)
        }), 500

@page_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_page', app_id=1, description='Récupérer une page par son ID', auto_register=True)
@trace_action(action_type="PAGE", code_prefix="PAGE")
def get_page(id):
    try:
        page = page_controller.get_page_by_id(id)
        if not page:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Page not found',
                    'fr': 'Page non trouvée'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Page retrieved successfully',
                'fr': 'Page récupérée avec succès'
            },
            'data': page_schema.dump(page)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving page',
                'fr': 'Erreur lors de la récupération de la page'
            },
            'details': str(e)
        }), 500

@page_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_page', app_id=1, description='Créer une nouvelle page', auto_register=True)
@trace_action(action_type="PAGE", code_prefix="PAGE")
@auto_set_user_fields()
def create_page():
    try:
        data = request.form.to_dict()
        icon_file = request.files.get('icon')
        
        page = page_controller.create_page(data, icon_file)
        return jsonify({
            'error': False,
            'message': {
                'en': 'Page created successfully',
                'fr': 'Page créée avec succès'
            },
            'data': page_schema.dump(page)
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
                'en': 'Error while creating page',
                'fr': 'Erreur lors de la création de la page'
            },
            'details': str(e)
        }), 500

@page_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_page', app_id=1, description='Mettre à jour une page', auto_register=True)
@trace_action(action_type="PAGE", code_prefix="PAGE")
@auto_set_user_fields()
def update_page(id):
    try:
        data = request.form.to_dict()
        icon_file = request.files.get('icon')
        
        page = page_controller.update_page(id, data, icon_file)
        if not page:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Page not found',
                    'fr': 'Page non trouvée'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Page updated successfully',
                'fr': 'Page mise à jour avec succès'
            },
            'data': page_schema.dump(page)
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
                'en': 'Error while updating page',
                'fr': 'Erreur lors de la mise à jour de la page'
            },
            'details': str(e)
        }), 500

@page_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_page', app_id=1, description='Supprimer une page', auto_register=True)
@trace_action(action_type="PAGE", code_prefix="PAGE")
def delete_page(id):
    try:
        result = page_controller.delete_page(id)
        if not result:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Page not found',
                    'fr': 'Page non trouvée'
                }
            }), 404
        return jsonify({
            'error': False,
            'message': {
                'en': 'Page deleted successfully',
                'fr': 'Page supprimée avec succès'
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while deleting page',
                'fr': 'Erreur lors de la suppression de la page'
            },
            'details': str(e)
        }), 500

@page_bp.route('/application/<int:app_id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_pages_by_application', app_id=1, description='Récupérer les pages d\'une application', auto_register=True)
@trace_action(action_type="PAGE", code_prefix="PAGE_APP")
def get_pages_by_application(app_id):
    try:
        pages = page_controller.get_pages_by_application(app_id)
        return jsonify({
            'error': False,
            'message': {
                'en': 'Pages retrieved successfully',
                'fr': 'Pages récupérées avec succès'
            },
            'data': pages_schema.dump(pages)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving pages',
                'fr': 'Erreur lors de la récupération des pages'
            },
            'details': str(e)
        }), 500

@page_bp.route('/application/<int:app_id>/add', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='add_pages_to_application', app_id=1, description='Ajouter des pages à une application', auto_register=True)
@trace_action(action_type="PAGE", code_prefix="PAGE_APP")
@auto_set_user_fields()
def add_pages_to_application(app_id):
    try:
        data = request.get_json()
        if not data or 'page_ids' not in data:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Page IDs are required',
                    'fr': 'Les identifiants de pages sont requis'
                }
            }), 400
            
        result = page_controller.add_pages_to_application(app_id, data['page_ids'])
        if not result:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Application not found',
                    'fr': 'Application non trouvée'
                }
            }), 404
            
        return jsonify({
            'error': False,
            'message': {
                'en': 'Pages added to application successfully',
                'fr': 'Pages ajoutées à l\'application avec succès'
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while adding pages to application',
                'fr': 'Erreur lors de l\'ajout des pages à l\'application'
            },
            'details': str(e)
        }), 500

@page_bp.route('/application/<int:app_id>/remove', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='remove_pages_from_application', app_id=1, description='Supprimer des pages d\'une application', auto_register=True)
@trace_action(action_type="PAGE", code_prefix="PAGE_APP")
@auto_set_user_fields()
def remove_pages_from_application(app_id):
    try:
        data = request.get_json()
        if not data or 'page_ids' not in data:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Page IDs are required',
                    'fr': 'Les identifiants de pages sont requis'
                }
            }), 400
            
        result = page_controller.remove_pages_from_application(app_id, data['page_ids'])
        if not result:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Pages not found in application',
                    'fr': 'Pages non trouvées dans l\'application'
                }
            }), 404
            
        return jsonify({
            'error': False,
            'message': {
                'en': 'Pages removed from application successfully',
                'fr': 'Pages retirées de l\'application avec succès'
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while removing pages from application',
                'fr': 'Erreur lors du retrait des pages de l\'application'
            },
            'details': str(e)
        }), 500 