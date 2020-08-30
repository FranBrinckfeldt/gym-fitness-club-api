from flask import Blueprint, jsonify, request, abort
from ..models import Usuario
from ..controller import user_register, user_login

users_blueprint = Blueprint('users_blueprint', __name__)

@users_blueprint.route('/register', methods=['POST'])
def post_user():
    user = request.get_json()
    return user_register(user)

@users_blueprint.route('/login', methods=['POST'])
def login_user():
    user = request.get_json()
    if user is not None and user.get('usuario') is not None and user.get('clave') is not None:
        return user_login(user['usuario'], user['clave'])
    else:
        abort(400)