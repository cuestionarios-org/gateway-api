from flask import Blueprint, request, jsonify
from services import  QuizService, AuthService
from middlewares.role_required import role_required
from services.proxy import proxy_service_request
import os

# Creación del blueprint para rutas relacionadas a competencias
competition_bp = Blueprint('competitions', __name__)
quiz_participation_bp = Blueprint('quiz-participation', __name__)

# Construcción de la URL base del microservicio de competencias
COMPETITION_SERVICE_URL = 'http://' + os.getenv('COMPETITION_HOST', 'localhost') + ':' + os.getenv('COMPETITION_PORT', '5013')


# -----------------------
# RUTAS PARA COMPETENCIAS
# -----------------------

@competition_bp.route('', methods=['GET'])
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
    Obtiene una competencia específica por su ID y enriquece los participantes con datos de usuario.

    Args:
        competition_id (int): Identificador de la competencia.

    Returns:
        Response: Datos de la competencia si existe.
    """
    # 1. Obtener detalle de la competencia
    resp, status = proxy_service_request("GET", f"/competitions/{competition_id}", service_url=COMPETITION_SERVICE_URL)
    if status != 200:
        return resp, status

    competition = resp.get_json() if hasattr(resp, 'get_json') else resp

    # 2. Enriquecer participantes usando bulk
    participants = competition.get("participants", [])
    print("Participants:", participants)
    participant_ids = [p.get("participant_id") for p in participants if p.get("participant_id") is not None]
    users_data, users_status = AuthService.get_users_by_ids(participant_ids)
    users_dict = {u["id"]: u for u in users_data.get("users", [])} if users_status == 200 else {}

    enriched_participants = []
    for p in participants:
        user_id = p.get("participant_id")
        user = users_dict.get(user_id, {})
        enriched = dict(p)  # Copia todos los datos originales
        enriched["username"] = user.get("username", "Desconocido")
        if "competition_id" in enriched:
            del enriched["competition_id"]
        enriched_participants.append(enriched)
    competition["participants"] = enriched_participants

    return jsonify(competition), 200


@competition_bp.route('', methods=['POST'])
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
@role_required(['usuario',"user", "admin", "moderator"])  # O solo 'user' si querés
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


# -----------------------------------------------
# 🟢 Proxy: Iniciar un quiz
# POST /quiz-participation/<competition_quiz_id>/participant/<participant_id>/start
# -----------------------------------------------
@quiz_participation_bp.route('/<int:competition_quiz_id>/participant/<int:participant_id>/start', methods=['POST'])
def proxy_start_quiz(competition_quiz_id, participant_id):
    return proxy_service_request(
        method="POST",
        path=f"/quiz-participation/{competition_quiz_id}/participant/{participant_id}/start",
        service_url=COMPETITION_SERVICE_URL
    )

# -----------------------------------------------
# 🟣 Proxy: Finalizar un quiz con respuestas
# POST /competitions/<competition_quiz_id>/participant/<participant_id>/finish
# -----------------------------------------------
@quiz_participation_bp.route('/<int:competition_quiz_id>/participant/<int:participant_id>/finish', methods=['POST'])
def proxy_finish_quiz(competition_quiz_id, participant_id):
    return proxy_service_request(
        method="POST",
        path=f"/quiz-participation/{competition_quiz_id}/participant/{participant_id}/finish",
        service_url=COMPETITION_SERVICE_URL,
        json=request.get_json(silent=True)
    )

# -----------------------------------------------
# 🔍 Proxy: Obtener respuestas de un participante
# GET /competitions/<competition_quiz_id>/participant/<participant_id>/answers
# -----------------------------------------------
@quiz_participation_bp.route('/<int:competition_quiz_id>/participant/<int:participant_id>/answers', methods=['GET'])
def proxy_get_user_answers(competition_quiz_id, participant_id):
    return proxy_service_request(
        method="GET",
        path=f"/quiz-participation/{competition_quiz_id}/participant/{participant_id}/answers",
        service_url=COMPETITION_SERVICE_URL
    )

# -----------------------------------------------
# 📋 Proxy: Obtener todas las respuestas del quiz (paginado)
# GET /competitions/<competition_quiz_id>/answers?page=1&per_page=50
# -----------------------------------------------
@quiz_participation_bp.route('/<int:competition_quiz_id>/answers', methods=['GET'])
def proxy_get_all_quiz_answers(competition_quiz_id):
    return proxy_service_request(
        method="GET",
        path=f"/quiz-participation/{competition_quiz_id}/answers",
        service_url=COMPETITION_SERVICE_URL,
        params=request.args
    )

# -----------------------------------------------
# 📚 Proxy: Obtener detalle completo del quiz por participante
# GET /competitions/<competition_quiz_id>/participant/<participant_id>
# -----------------------------------------------
@quiz_participation_bp.route('/<int:competition_quiz_id>/participant/<int:participant_id>', methods=['GET'])
def proxy_get_complete_quiz_by_user(competition_quiz_id, participant_id):
    return proxy_service_request(
        method="GET",
        path=f"/quiz-participation/{competition_quiz_id}/participant/{participant_id}",
        service_url=COMPETITION_SERVICE_URL
    )

# -----------------------------------------------
# 📚 Proxy: Obtener las competencias del usuario
# GET /competitions/user
# -----------------------------------------------
@competition_bp.route('/users', methods=['GET'])
@role_required(['usuario','user','admin','moderator'])
def get_user_competitions(token_data):
    """
    Devuelve las competencias en las que el usuario está inscrito,
    las que ha completado y las que aún puede inscribirse.
    """
    user_id = token_data['user_id']
    # Proxear a: GET /users/{user_id}/competitions?include=pending,active,finished
    return proxy_service_request(
        "GET",
        f"/competitions/users/{user_id}",
        service_url=COMPETITION_SERVICE_URL,
        params=request.args  # podríamos usar ?status=pending|active|finished
    )
