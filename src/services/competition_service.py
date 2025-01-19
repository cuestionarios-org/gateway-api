import requests
import os
from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class CompetitionService:
    COMPETITION_URL = os.getenv('COMPETITION_SERVICE_URL') + '/competitions'

    @staticmethod
    def list_competitions():
        """
        Lista todas las competencias asegurando que cada una tenga la clave 'quizzes'.
        """
        try:
            response = requests.get(f"{CompetitionService.COMPETITION_URL}")
            if response.status_code == 200:
                competitions = response.json()
                # Agregar clave 'quizzes' si no está presente
                for competition in competitions:
                    if 'quizzes' not in competition:
                        competition['quizzes'] = []
                return competitions, 200
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de competencias."}, 503
        except Exception as e:
            logger.error(f"Error al listar competencias: {e}")
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def create_competition(data):
        """
        Crea una nueva competencia. Puede incluir o no una lista de cuestionarios.
        """
        try:
            response = requests.post(f"{CompetitionService.COMPETITION_URL}", json=data)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de competencias."}, 503
        except Exception as e:
            logger.error(f"Error al crear competencia: {e}")
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def get_competition_by_id(competition_id):
        """
        Obtiene una competencia por su ID.
        """
        try:
            response = requests.get(f"{CompetitionService.COMPETITION_URL}/{competition_id}")
            if response.status_code == 200:
                competition = response.json()
                # Asegurarse de que la clave 'quizzes' exista
                if 'quizzes' not in competition:
                    competition['quizzes'] = []
                return competition, 200
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de competencias."}, 503
        except Exception as e:
            logger.error(f"Error al obtener competencia {competition_id}: {e}")
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def update_competition(competition_id, data):
        """
        Actualiza una competencia existente. Puede incluir o no la lista de cuestionarios.
        """
        try:
            response = requests.put(f"{CompetitionService.COMPETITION_URL}/{competition_id}", json=data)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de competencias."}, 503
        except Exception as e:
            logger.error(f"Error al actualizar competencia {competition_id}: {e}")
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def delete_competition(competition_id):
        """
        Elimina una competencia por su ID.
        """
        try:
            response = requests.delete(f"{CompetitionService.COMPETITION_URL}/{competition_id}")
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de competencias."}, 503
        except Exception as e:
            logger.error(f"Error al eliminar competencia {competition_id}: {e}")
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500
