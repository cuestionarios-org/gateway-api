from flask import Blueprint, request, jsonify
from services import CompetitionService, QuizService
from middlewares.role_required import role_required

competition_bp = Blueprint('competitions', __name__)

# Rutas para competencias

@competition_bp.route('/', methods=['GET'])
def get_all_competitions():
    """
    Lista todas las competencias.
    """
    data, status = CompetitionService.list_competitions()
    return jsonify(data), status


@competition_bp.route('/', methods=['POST'])
@role_required(["admin", "moderator"])
def create_competition(token_data):
    """
    Crea una nueva competencia, validando que los quizzes existan.

    Args:
        token_data (dict): Información del usuario autenticado.

    Returns:
        dict: La competencia creada o un mensaje de error.
        int: El estatus de la respuesta.
    """
    data = request.json
    user_id = token_data.get("user_id")
    data["created_by"] = user_id

    # Extraer los quiz_id de la solicitud
    quiz_ids = [quiz["quiz_id"] for quiz in data.get("quizzes", [])]

    # Validar que los quizzes existen
    quizzes_exist, error_message = QuizService.validate_quizzes_exist(quiz_ids)

    if not quizzes_exist:
        return jsonify({"message": "Algunos quizzes no existen", "error": error_message}), 400

    # Si todos los quizzes existen, continuar con la creación de la competencia
    response_data, status = CompetitionService.create_competition(data)
    return jsonify(response_data), status


@competition_bp.route('/<int:competition_id>', methods=['GET'])
@role_required(["admin", "moderator"])
def get_competition_by_id(competition_id):
    """
    Obtiene una competencia por su ID.

    Args:
        competition_id (int): Identificador de la competencia.

    Returns:
        dict: La competencia obtenida.
        int: El estatus de la respuesta.
    """
    data, status = CompetitionService.get_competition_by_id(competition_id)
    return jsonify(data), status


@competition_bp.route('/<int:competition_id>', methods=['PUT'])
@role_required(["admin", "moderator"])
def update_competition(competition_id, token_data):
    """
    Edita una competencia.

    Args:
        competition_id (int): Identificador de la competencia.
        token_data (dict): Información del usuario autenticado.

    Returns:
        dict: La competencia actualizada.
        int: El estatus de la respuesta.
    """
    data = request.json
    user_id = token_data.get("user_id")
    data["modified_by"] = user_id

    response_data, status = CompetitionService.update_competition(competition_id, data)
    return jsonify(response_data), status


@competition_bp.route('/<int:competition_id>', methods=['DELETE'])
@role_required(["admin", "moderator"])
def delete_competition(competition_id):
    """
    Elimina una competencia por su ID.

    Args:
        competition_id (int): Identificador de la competencia.

    Returns:
        dict: Mensaje de éxito o error.
        int: El estatus de la respuesta.
    """
    response_data, status = CompetitionService.delete_competition(competition_id)
    return jsonify(response_data), status
