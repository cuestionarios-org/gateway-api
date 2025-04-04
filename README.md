# 🚀 **API Gateway para Sistema de Cuestionarios en Microservicios**

## 📚 **Descripción General**
El **API Gateway** es el punto de entrada centralizado para el sistema de cuestionarios en una arquitectura basada en microservicios. Maneja autenticación, autorización, enrutamiento de solicitudes y comunicación segura entre servicios, asegurando eficiencia, seguridad y escalabilidad. Diseñado con una arquitectura modular para facilitar la extensión y el mantenimiento.

---

## 🛠️ **Tecnologías Utilizadas**
- **Python** (Flask como framework principal)
- **PyJWT** (Manejo de autenticación JWT)
- **Docker** (Contenedorización)
- **Docker Compose** (Orquestación de servicios)
- **pytest** (Pruebas automatizadas)
- **logging** (Registro de logs centralizado)

---

## 📂 **Estructura del Proyecto**
La estructura actual del proyecto sigue una organización clara y modular:

```
api-gateway/
├── src/
│   ├── config/
│   │   ├── __init__.py           # Inicializador del módulo
│   │   ├── config.py             # Configuraciones globales
│   │
│   ├── routes/
│   │   ├── __init__.py           # Inicializador del módulo
│   │   ├── auth_routes.py        # Rutas relacionadas con la autenticación
│   │   ├── register_routes.py    # Rutas para registro de usuarios
│   │
│   ├── services/
│   │   ├── __init__.py           # Inicializador del módulo
│   │   ├── auth_service.py       # Lógica para autenticación y autorización
│   │
│   ├── utils/
│   │   ├── __init__.py           # Inicializador del módulo
│   │   ├── error_handlers.py     # Manejadores de errores personalizados
│   │   ├── logger.py             # Configuración y gestión de logs
│   │
│   ├── middlewares/
│   │   ├── __init__.py           # Inicializador del módulo
│   │   ├── jwt_middleware.py     # Middleware para validación JWT
│   │   ├── role_required.py      # Middleware para validación de roles
│   │
│   ├── tests/
│   │   ├── __init__.py           # Inicializador del módulo
│   │   ├── test_auth.py          # Pruebas para autenticación
│   │   ├── test_middlewares.py   # Pruebas para middlewares
│   │
│   ├── main.py                   # Punto de entrada principal
├── requirements.txt              # Dependencias del proyecto
├── Dockerfile                    # Configuración para construir la imagen Docker
├── docker-compose.yml            # Orquestación de servicios con Docker Compose
├── .env                          # Variables de entorno
├── pytest.ini                    # Configuración para pytest
├── .gitignore                    # Archivos y carpetas a ignorar en git
├── readme.md                     # Documentación del proyecto
```

---

## 🧑‍💻 **Primeros Pasos**

### 1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/api-gateway.git
cd api-gateway
```

### 2. Crear y activar un entorno virtual:
```bash
python -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`
```

### 3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno:
Crea un archivo `.env` en la raíz del proyecto y agrega las variables necesarias:
```env
REHACER
```

### 5. Ejecutar la aplicación:
```bash
python src/main.py
```

### 6. Ejecutar las pruebas para asegurar que todo funcione correctamente:
```bash
pytest tests/
```

---

## 🔑 **Autenticación y Autorización**
- **JWT (JSON Web Token):** Para usuarios externos.
- **Middleware de Roles:** Garantiza acceso restringido según el nivel del usuario.
- **Manejadores de Errores:** Detecta y responde a problemas como tokens inválidos o expirados.

### 🧠 **Flujo de Autenticación**
1. Las solicitudes de usuarios deben incluir un **Token JWT** en el encabezado.
2. Las solicitudes se verifican mediante el **Middleware JWT**.
3. Si se requiere, el middleware de roles valida permisos específicos antes de procesar la solicitud.

---

## 📜 **Rutas Principales**
Las rutas están organizadas en la carpeta `routes/`. Algunas de las más importantes son:

- **Autenticación:** `/auth`
- **Registro:** `/register`
- **Servicios Internos:** `/quiz/internal`

---

## 🐳 **Despliegue con Docker Compose**
### Construir y ejecutar el proyecto:
```bash
docker-compose up --build
```

### 🌍 **Acceder al API Gateway:**
```plaintext
http://localhost:5000/
```

---

## ✅ **Pruebas Automatizadas**
Ejecuta las pruebas para validar la estabilidad y el correcto funcionamiento del proyecto:
```bash
pytest tests/
```

---

## 📊 **Variables de Entorno (.env)**
```env
REHACER
```

---

## 🌟 **Posibles Mejoras Futuras**
- Implementar **ratelimiters** para prevenir abuso de endpoints.
- Agregar soporte para **OpenAPI** (Swagger) para documentación automática.
- Integración con un sistema de monitoreo como **Prometheus**.
- Configurar **CI/CD** con GitHub Actions para despliegue automático.
- Agregar **cacheo** de respuestas con Redis.

---

## 🤝 **Contribuciones**
¡Las contribuciones son bienvenidas! Si encuentras un problema o tienes sugerencias, abre un **Issue** o envía un **Pull Request**.

---

## 📝 **Licencia**
Este proyecto está bajo la licencia **MIT**.

---

## 📬 **Contacto**
- **Desarrollador:** [Tu Nombre]
- **Email:** [tu.email@example.com]
- **LinkedIn:** [Tu Perfil]

---

¡Gracias por usar el **API Gateway** del sistema de cuestionarios! 🚀🔒

