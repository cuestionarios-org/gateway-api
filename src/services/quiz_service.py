import requests
import os
from config.config import Config
from utils.logger import get_logger
logger = get_logger(__name__)


class QuizService:
    """
    Clase para interactuar con el servicio de cuestionarios.
    Contiene métodos para listar, crear, obtener y actualizar cuestionarios.
    """
    # Formaciono de la URL del servicio de cuestionarios
    QA_SERVICE_URL = 'http://' + os.getenv('QA_HOST', 'localhost') + ':' + os.getenv('QA_PORT', '5012')
    
    QA_URL = QA_SERVICE_URL + '/quizzes'
    @staticmethod
    def list_quizzes(quiz_ids=None):
        """
        Lista todos los cuestionarios o solo los especificados en 'quiz_ids'.
        """
        try:
            params = {"quiz_ids": ",".join(map(str, quiz_ids))} if quiz_ids else {}
            response = requests.get(f"{QuizService.QA_URL}", params=params)

            if response.status_code == 200:
                quizzes = response.json()
                # Asegurar que todos los quizzes tengan la clave 'questions'
                for quiz in quizzes:
                    if 'questions' not in quiz:
                        quiz['questions'] = []
                return quizzes, 200

            return response.json(), response.status_code

        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de cuestionarios."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def list_quizzesOLD():
        """
        Lista todos los cuestionarios asegurando que cada uno tenga la clave 'quiz'.
        """
        try:
            response = requests.get(f"{QuizService.QA_URL}")
            if response.status_code == 200:
                quizzes = response.json()
                # Agregar clave 'questions' si no está presente
                for quiz in quizzes:
                    if 'questions' not in quiz:
                        quiz['questions'] = []
                return quizzes, 200
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de cuestionarios."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def create_quiz(data):
        """
        Crea un nuevo cuestionario.
        """
        try:
            response = requests.post(f"{QuizService.QA_URL}", json=data)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de cuestionarios."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def get_quiz_by_id(quiz_id):
        """
        Obtiene un cuestionario por su ID.
        """
        try:
            response = requests.get(f"{QuizService.QA_URL}/{quiz_id}")
            if response.status_code == 200:
                quiz = response.json()
                # Agregar clave 'quiz' si no está presente
                if 'quiz' not in quiz:
                    quiz['quiz'] = []
                return quiz, 200
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de cuestionarios."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def update_quiz(quiz_id, data):
        """
        Actualiza un cuestionario existente.
        """
        try:
            response = requests.put(f"{QuizService.QA_URL}/{quiz_id}", json=data)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de cuestionarios."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def validate_quizzes_exist(quiz_ids):
        """
        Valida que los quizzes especificados existen en el sistema.

        Args:
            quiz_ids (list): Lista de IDs de quizzes a validar.

        Returns:
            tuple: (bool, str) -> True si todos existen, False con mensaje de error si alguno no existe.
        """
        try:
            response = requests.get(f"{QuizService.QA_URL}", params={"quiz_ids": ",".join(map(str, quiz_ids))})
            
            if response.status_code != 200:
                return False, f"Error al consultar el servicio de quizzes: {response.text}"

            existing_quizzes = {quiz["id"] for quiz in response.json()}  # IDs existentes

            # Verificar qué quizzes no existen
            missing_quizzes = [quiz_id for quiz_id in quiz_ids if quiz_id not in existing_quizzes]

            if missing_quizzes:
                return False, f"Los siguientes quizzes no existen: {missing_quizzes}"

            return True, ""

        except requests.exceptions.ConnectionError:
            return False, "Error de conexión con el servicio de quizzes."
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
