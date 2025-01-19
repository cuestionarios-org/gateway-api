from flask import Blueprint, request, jsonify
from services import QuizService
from middlewares.role_required import role_required

quiz_bp = Blueprint('quizzes', __name__)

# Rutas para cuestionarios

@quiz_bp.route('/', methods=['GET'])
def get_all_quizzes():
    """
    Lista todos los cuestionarios.
    """
    data, status = QuizService.list_quizzes()
    return jsonify(data), status


@quiz_bp.route('/', methods=['POST'])
@role_required(["admin", "moderator"])
def create_quiz(token_data):
    """
    Crea un nuevo cuestionario.

    Args:
        token_data (dict): Información del usuario autenticado.

    Returns:
        dict: El cuestionario creado.
        int: El estatus de la respuesta.
    """
    data = request.json
    user_id = token_data.get("user_id")
    data["quiz"]["created_by"] = user_id

    response_data, status = QuizService.create_quiz(data)
    return jsonify(response_data), status


@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
@role_required(["admin", "moderator"])
def get_quiz_by_id(quiz_id):
    """
    Obtiene un cuestionario por su ID.

    Args:
        quiz_id (int): Identificador del cuestionario.

    Returns:
        dict: El cuestionario obtenido.
        int: El estatus de la respuesta.
    """
    data, status = QuizService.get_quiz_by_id(quiz_id)
    return jsonify(data), status


@quiz_bp.route('/<int:quiz_id>', methods=['PUT'])
@role_required(["admin", "moderator"])
def update_quiz(quiz_id, token_data):
    """
    Edita un cuestionario.

    Args:
        quiz_id (int): Identificador del cuestionario.
        token_data (dict): Información del usuario autenticado.

    Returns:
        dict: El cuestionario actualizado.
        int: El estatus de la respuesta.
    """
    data = request.json
    user_id = token_data.get("user_id")
    data["quiz"]["modified_by"] = user_id

    response_data, status = QuizService.update_quiz(quiz_id, data)
    return jsonify(response_data), status
