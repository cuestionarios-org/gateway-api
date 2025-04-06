from flask import Blueprint, request, jsonify
from services import  QuizService
from middlewares.role_required import role_required
from services.proxy import proxy_service_request
import os

# Creación del blueprint para rutas relacionadas a competencias
competition_bp = Blueprint('competitions', __name__)

# Construcción de la URL base del microservicio de competencias
COMPETITION_SERVICE_URL = 'http://' + os.getenv('COMPETITION_HOST', 'localhost') + ':' + os.getenv('COMPETITION_PORT', '5013')


# -----------------------
# RUTAS PARA COMPETENCIAS
# -----------------------

@competition_bp.route('/', methods=['GET'])
def get_all_competitions():
    """
    Lista todas las competencias disponibles.

    Returns:
        Response: Lista de competencias en formato JSON.
    """
    return proxy_service_request("GET", "/competitions", service_url=COMPETITION_SERVICE_URL)


@competition_bp.route('/<int:competition_id>', methods=['GET'])
@role_required(["admin", "moderator"])
def get_competition_by_id(competition_id):
    """
    Obtiene una competencia específica por su ID.

    Args:
        competition_id (int): Identificador de la competencia.

    Returns:
        Response: Datos de la competencia si existe.
    """
    return proxy_service_request("GET", f"/competitions/{competition_id}", service_url=COMPETITION_SERVICE_URL)


@competition_bp.route('/', methods=['POST'])
@role_required(["admin", "moderator"])
def create_competition(token_data):
    """
    Crea una nueva competencia. Antes de crearla, valida que todos los quizzes referenciados existan.

    Args:
        token_data (dict): Información del usuario autenticado extraída por el decorador.

    Returns:
        Response: Competencia creada o mensaje de error si falló la validación.
    """
    data = request.json
    user_id = token_data.get("user_id")

    # Se guarda quién creó la competencia
    data["created_by"] = user_id

    # Extraer los IDs de quizzes enviados
    quiz_ids = [quiz["quiz_id"] for quiz in data.get("quizzes", [])]

    # Verificar que los quizzes existen antes de reenviar al microservicio
    quizzes_exist, error_message = QuizService.validate_quizzes_exist(quiz_ids)
    if not quizzes_exist:
        return jsonify({"message": "Algunos quizzes no existen", "error": error_message}), 400

    # Reenviar la solicitud al microservicio correspondiente
    return proxy_service_request("POST", "/competitions", service_url=COMPETITION_SERVICE_URL, json=data)


@competition_bp.route('/<int:competition_id>', methods=['PUT'])
@role_required(["admin", "moderator"])
def update_competition(competition_id, token_data):
    """
    Actualiza los datos de una competencia específica. Si se incluyen quizzes, también se validan.

    Args:
        competition_id (int): Identificador de la competencia a actualizar.
        token_data (dict): Información del usuario autenticado.

    Returns:
        Response: Competencia actualizada o mensaje de error si hay problemas de validación.
    """
    data = request.json
    user_id = token_data.get("user_id")

    # Se guarda quién realizó la modificación
    data["modified_by"] = user_id

    # Si se enviaron quizzes en la solicitud, validar su existencia
    if "quizzes" in data:
        quiz_ids = [quiz.get("quiz_id") for quiz in data["quizzes"] if "quiz_id" in quiz]
        if quiz_ids:
            quizzes_exist, error_message = QuizService.validate_quizzes_exist(quiz_ids)
            if not quizzes_exist:
                return jsonify({"message": "Algunos quizzes no existen", "error": error_message}), 400

    return proxy_service_request("PUT", f"/competitions/{competition_id}", service_url=COMPETITION_SERVICE_URL, json=data)

# --------------------------------------------
# ✅ Admin/mod inscribe a un participante
# --------------------------------------------
@competition_bp.route('/<int:competition_id>/participants/<int:participant_id>', methods=['POST'])
@role_required(["admin", "moderator"])
def proxy_add_participant_as_admin(competition_id, participant_id):
    """
    Proxy: Inscribe un participante en una competencia (admin/moderador).

    Método: POST
    Endpoint: /competitions/<competition_id>/participants/<participant_id>

    Solo accesible por roles 'admin' o 'moderator'.
    """
    return proxy_service_request(
        "POST",
        f"/competitions/{competition_id}/participants/{participant_id}",
        service_url=COMPETITION_SERVICE_URL
    )

# --------------------------------------------
# ✅ Usuario se autoinscribe (ID desde token)
# --------------------------------------------
@competition_bp.route('/<int:competition_id>/participants', methods=['POST'])
@role_required(["user", "admin", "moderator"])  # O solo 'user' si querés
def proxy_self_register_to_competition(competition_id, token_data):
    """
    Proxy: Usuario autenticado se inscribe en una competencia.

    Método: POST
    Endpoint: /competitions/<competition_id>/participants

    El ID del usuario se obtiene del token.
    """
    user_id = token_data.get("user_id")
    return proxy_service_request(
        "POST",
        f"/competitions/{competition_id}/participants/{user_id}",
        service_url=COMPETITION_SERVICE_URL
    )


@competition_bp.route('/<int:competition_id>/ranking', methods=['GET'])
def proxy_get_competition_ranking(competition_id):
    """
    Proxy: Obtiene el ranking de una competencia.

    Método: GET
    Endpoint: /competitions/<competition_id>/ranking
    """
    return proxy_service_request(
        "GET",
        f"/competitions/{competition_id}/ranking",
        service_url=COMPETITION_SERVICE_URL
    )
