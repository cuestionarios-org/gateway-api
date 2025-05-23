from flask import Blueprint, request, jsonify
from services import AuthService
from middlewares.role_required import role_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def auth_login():
    data, status = AuthService.login(request.json)
    return jsonify(data), status

@auth_bp.route('/register', methods=['POST'])
def auth_register():
    data, status = AuthService.register(request.json)
    return jsonify(data), status


# creacion de ruta /me para obtener los datos del usuario autenticado

@auth_bp.route('/me', methods=['GET'])
def auth_me():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    data, status = AuthService.me(token)
    return jsonify(data), status



@auth_bp.route('/list', methods=['GET'])
@role_required(["admin", "moderator"])
def auth_list_users():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    data, status = AuthService.list_users(token)
    return jsonify(data), status

@auth_bp.route('/protected', methods=['GET'])
def auth_protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    data, status = AuthService.protected_route(token)
    return jsonify(data), status