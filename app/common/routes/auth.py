from flask import Blueprint, request, jsonify
from app.common.controllers.auth_controller import AuthController
from app.common.schemas import UtilisateurSchema
from app.common.controllers.trace_controller import TraceController

auth_bp = Blueprint('auth', __name__)
auth_controller = AuthController()
trace_controller = TraceController()
utilisateur_schema = UtilisateurSchema()

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authentifier un utilisateur"""
    try:
        if not request.is_json:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Request must be JSON',
                    'fr': 'La requête doit être au format JSON'
                }
            }), 400

        data = request.get_json()
        login = data.get('login')
        password = data.get('password')

        # Validation des champs requis
        if not login or not password:
            return jsonify({
                'error': True,
                'message': {
                    'en': 'Login and password are required',
                    'fr': 'Login et mot de passe sont requis'
                }
            }), 400

        result, status_code = auth_controller.login(login, password)
        
        if result.get('error'):
            return jsonify(result), status_code

        # Sérialiser l'utilisateur avant de le renvoyer
        utilisateur = result['data']['utilisateur']
        result['data']['utilisateur'] = utilisateur_schema.dump(utilisateur)
        
        # Créer la trace après un login réussi
        if not result.get('error') and status_code == 200:
            trace_controller.create_trace({
                'id_utilisateur': utilisateur.id_utilisateur,
                'action': 'AUTH',
                'code': "AUTH_LOGIN",
                'detail': f"Connexion de l'utilisateur {utilisateur.login}",
                'end_point': "/api/auth/login",
                'param': f"username={utilisateur.login}"
            })

        return jsonify(result), status_code

    except Exception as e:
        return jsonify({
            'error': True,
            'message': {
                'en': 'Error during authentication',
                'fr': 'Erreur lors de l\'authentification'
            },
            'details': str(e)
        }), 500 