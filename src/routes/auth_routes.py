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
