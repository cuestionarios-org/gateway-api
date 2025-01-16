from flask import Blueprint, request, jsonify
from services.question_service import QuestionService
from middlewares.role_required import role_required

qa_bp = Blueprint('questions', __name__)


# rutas para categorias
@qa_bp.route('/categories/', methods=['GET'])
def get_all_categories():
    data, status = QuestionService.list_categories()
    return jsonify(data), status

@qa_bp.route('/categories/', methods=['POST'])
@role_required(["admin", "moderator"])
def create_category():
    data = request.json
    category_data, status = QuestionService.create_category(data)
    return jsonify(category_data), status

# rutas para preguntas
@qa_bp.route('/', methods=['GET'])
def get_all_questions():
    data, status = QuestionService.list_questions()
    return jsonify(data), status


@qa_bp.route('/category/<int:category_id>', methods=['GET'])
@role_required(["admin", "moderator"])
def questions_list_by_category(category_id):

    data, status = QuestionService.list_questions_by_category(category_id)
    return jsonify(data), status

from flask import Blueprint, request, jsonify
from services.question_service import QuestionService
from middlewares.role_required import role_required


# Crear una pregunta con respuestas
@qa_bp.route('/', methods=['POST'])
@role_required(["admin", "moderator"])
def create_question(token_data):
    """
    Crea una pregunta y sus respuestas

    Args:
        token_data (dict): Informaci n del usuario autenticado

    Returns:
        dict: La pregunta y sus respuestas creadas
        int: El estatus de la respuesta
    """
    data = request.json
    # Incluimos el `created_by` basado en el usuario autenticado
    user_id = token_data.get("user_id")
    data["question"]["created_by"] = user_id

    response_data, status = QuestionService.create_question_with_answers(data)
    return jsonify(response_data), status

# Obtener una pregunta por ID
@qa_bp.route('/<int:question_id>', methods=['GET'])
@role_required(["admin", "moderator"])
def get_question_by_id(question_id):
    """
    Obtiene una pregunta por su ID

    Args:
        question_id (int): Identificador de la pregunta

    Returns:
        dict: La pregunta y sus respuestas
        int: El estatus de la respuesta
    """
    data, status = QuestionService.get_question_by_id(question_id)
    return jsonify(data), status

# Editar una pregunta y sus respuestas
@qa_bp.route('/<int:question_id>', methods=['PUT'])
@role_required(["admin", "moderator"])
def update_question(question_id, token_data):
    """
    Edita una pregunta y sus respuestas

    Args:
        question_id (int): Identificador de la pregunta
        token_data (dict): Informaci n del usuario autenticado

    Returns:
        dict: La pregunta actualizada y sus respuestas
        int: El estatus de la respuesta
    """
    data = request.json
    # Incluimos el `modified_by` basado en el usuario autenticado
    user_id = token_data.get("user_id")
    data["question"]["modified_by"] = user_id

    response_data, status = QuestionService.update_question_with_answers(question_id, data)
    return jsonify(response_data), status
