from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def auth_login():
    data, status = AuthService.login(request.json)
    return jsonify(data), status

@auth_bp.route('/register', methods=['POST'])
def auth_register():
    data, status = AuthService.register(request.json)
    return jsonify(data), status

@auth_bp.route('/list', methods=['GET'])
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