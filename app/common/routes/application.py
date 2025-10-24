from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.common.controllers.application_controller import ApplicationController
from app.common.schemas import ApplicationSchema
from app.common.decorators import api_fonction, trace_action, auto_set_user_fields

application_bp = Blueprint('application', __name__)
application_controller = ApplicationController()
application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)

@application_bp.route('/', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_applications', app_id=1, description='Récupérer toutes les applications', auto_register=True)
@trace_action(action_type="APPLICATION", code_prefix="APP")
def get_applications():
    try:
        applications = application_controller.get_all_applications()
        return jsonify({
            'error': False,
            'message': {
                'en': 'Applications retrieved successfully',
                'fr': 'Applications récupérées avec succès'
            },
            'data': applications_schema.dump(applications)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving applications',
                'fr': 'Erreur lors de la récupération des applications'
            },
            'details': str(e)
        }), 500

@application_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@api_fonction(nom_fonction='get_application', app_id=1, description='Récupérer une application par son ID', auto_register=True)
@trace_action(action_type="APPLICATION", code_prefix="APP")
def get_application(id):
    try:
        application = application_controller.get_application_by_id(id)
        if not application:
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
                'en': 'Application retrieved successfully',
                'fr': 'Application récupérée avec succès'
            },
            'data': application_schema.dump(application)
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while retrieving application',
                'fr': 'Erreur lors de la récupération de l\'application'
            },
            'details': str(e)
        }), 500

@application_bp.route('/', methods=['POST'])
@jwt_required()
@api_fonction(nom_fonction='create_application', app_id=1, description='Créer une nouvelle application', auto_register=True)
@trace_action(action_type="APPLICATION", code_prefix="APP")
@auto_set_user_fields()
def create_application():
    try:
        data = request.form.to_dict()
        icon_file = request.files.get('app_icon')
        
        application = application_controller.create_application(data, icon_file)
        return jsonify({
            'error': False,
            'message': {
                'en': 'Application created successfully',
                'fr': 'Application créée avec succès'
            },
            'data': application_schema.dump(application)
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
                'en': 'Error while creating application',
                'fr': 'Erreur lors de la création de l\'application'
            },
            'details': str(e)
        }), 500

@application_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@api_fonction(nom_fonction='update_application', app_id=1, description='Mettre à jour une application', auto_register=True)
@trace_action(action_type="APPLICATION", code_prefix="APP")
@auto_set_user_fields()
def update_application(id):
    try:
        data = request.form.to_dict()
        icon_file = request.files.get('app_icon')
        
        application = application_controller.update_application(id, data, icon_file)
        if not application:
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
                'en': 'Application updated successfully',
                'fr': 'Application mise à jour avec succès'
            },
            'data': application_schema.dump(application)
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
                'en': 'Error while updating application',
                'fr': 'Erreur lors de la mise à jour de l\'application'
            },
            'details': str(e)
        }), 500

@application_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@api_fonction(nom_fonction='delete_application', app_id=1, description='Supprimer une application', auto_register=True)
@trace_action(action_type="APPLICATION", code_prefix="APP")
def delete_application(id):
    try:
        result = application_controller.delete_application(id)
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
                'en': 'Application deleted successfully',
                'fr': 'Application supprimée avec succès'
            }
        })
    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error while deleting application',
                'fr': 'Erreur lors de la suppression de l\'application'
            },
            'details': str(e)
        }), 500 