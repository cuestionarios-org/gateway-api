import requests
import os
from config.config import Config
from utils.logger import get_logger
logger = get_logger(__name__)


class QuestionService:

    """
    Clase para interactuar con el servicio de preguntas y respuestas.   
    Contiene métodos para listar preguntas, crear preguntas y respuestas, y acceder a categorías.
    """
    # Formaciono de la URL del servicio de preguntas y respuestas
    QA_SERVICE_URL ='http://' + os.getenv('QA_HOST','localhost') + ':' + os.getenv('QA_PORT','5012')

    QA_URL = QA_SERVICE_URL + '/questions'
    QA_CATEGORIES_URL = QA_SERVICE_URL + '/categories'

    @staticmethod
    def list_categories():
        try:
            # Realiza la solicitud al servicio de autenticación
            response = requests.get(f"{QuestionService.QA_CATEGORIES_URL}")
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de preguntas y respuestas."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def create_category(data):
        try:
            
            # Realiza la solicitud al servicio de autenticación
            response = requests.post(f"{QuestionService.QA_CATEGORIES_URL}", json=data)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de autenticación."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def list_questions():
        try:
            # Realiza la solicitud al servicio de autenticación
            response = requests.get(f"{QuestionService.QA_URL}")
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de preguntas y respuestas."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

  
    @staticmethod
    def list_questions_by_category(category_id):
        try:
                       
            # Realiza la solicitud al servicio de autenticación
            response = requests.get(f"{QuestionService.QA_URL}/category/{category_id}")
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de autenticación."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

        
    @staticmethod
    def create_question_with_answers(data):
        try:
            response = requests.post(f"{QuestionService.QA_URL}", json=data)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de preguntas y respuestas."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def get_question_by_id(question_id):
        try:
            response = requests.get(f"{QuestionService.QA_URL}/{question_id}")
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de preguntas y respuestas."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500

    @staticmethod
    def update_question_with_answers(question_id, data):
        print(data)
        try:
            response = requests.put(f"{QuestionService.QA_URL}/{question_id}", json=data)
            return response.json(), response.status_code
        except requests.exceptions.ConnectionError:
            return {"message": "Error de conexión con el servicio de preguntas y respuestas."}, 503
        except Exception as e:
            return {"message": "Error al procesar la solicitud.", "error": str(e)}, 500
