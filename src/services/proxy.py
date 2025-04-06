import requests
from flask import jsonify, request

def proxy_service_request(method, path, json=None, params=None, service_url=None, headers=None):
    """
    Encaminador (proxy) para enviar solicitudes HTTP a un microservicio.

    Args:
        method (str): Método HTTP (GET, POST, PUT, DELETE, etc.).
        path (str): Ruta del microservicio, por ejemplo "/competitions".
        json (dict, optional): Cuerpo de la solicitud, si aplica.
        params (dict, optional): Parámetros de consulta (query params).
        service_url (str): URL base del microservicio.
        headers (dict, optional): Headers adicionales a enviar (opcional).

    Returns:
        Response: Respuesta reenviada del microservicio.
    """
    url = f"{service_url}{path}"

    # Headers base
    forwarded_headers = headers.copy() if headers else {}

    # Si el cliente envió un token JWT, lo reenviamos
    auth_header = request.headers.get('Authorization')
    if auth_header:
        forwarded_headers['Authorization'] = auth_header

    try:
        # Enviamos la solicitud al microservicio
        resp = requests.request(
            method,
            url,
            json=json,
            params=params,
            headers=forwarded_headers
        )

        # Devolvemos la respuesta del microservicio tal como vino
        return jsonify(resp.json()), resp.status_code

    except requests.exceptions.ConnectionError:
        # Error de conexión con el microservicio
        return jsonify({"message": "Error al conectar con el microservicio"}), 503
    except ValueError:
        # Si el microservicio no responde con JSON válido
        return jsonify({"message": "Respuesta no válida del microservicio"}), 502
