# 🚀 API Gateway - Sistema de Cuestionarios

API Gateway que sirve como punto de entrada centralizado para el sistema de cuestionarios, gestionando autenticación, autorización y enrutamiento de solicitudes.

## 📚 Características Principales

- Autenticación JWT
- Control de acceso basado en roles
- Rate limiting
- Manejo centralizado de errores
- Logging
- Redirección de peticiones a microservicios

## 🛠️ Endpoints Principales

### 🔑 Autenticación
```http
POST /auth/login
POST /auth/register
GET /auth/protected    # Ruta protegida de prueba
GET /auth/list        # Lista usuarios (admin/moderator)
```

### 📝 Cuestionarios
```http
GET    /quizzes            # Lista todos los cuestionarios
POST   /quizzes            # Crea nuevo cuestionario (admin/moderator)
GET    /quizzes/:id        # Obtiene un cuestionario específico
PUT    /quizzes/:id        # Actualiza un cuestionario (admin/moderator)
```

### ❓ Preguntas
```http
GET    /questions                      # Lista todas las preguntas
POST   /questions                      # Crea nueva pregunta (admin/moderator)
GET    /questions/:id                  # Obtiene una pregunta específica
PUT    /questions/:id                  # Actualiza una pregunta (admin/moderator)
GET    /questions/categories           # Lista categorías de preguntas
POST   /questions/categories           # Crea nueva categoría (admin/moderator)
GET    /questions/category/:id         # Lista preguntas por categoría
```

### 🏆 Competencias
```http
GET    /competitions                   # Lista todas las competencias
POST   /competitions                   # Crea nueva competencia (admin/moderator)
GET    /competitions/:id               # Obtiene una competencia específica
PUT    /competitions/:id               # Actualiza una competencia (admin/moderator)
POST   /competitions/:id/participants  # Auto-inscripción a competencia
GET    /competitions/:id/ranking       # Obtiene ranking de competencia
```

### 📋 Participación en Cuestionarios
```http
POST   /quiz-participation/:quizId/participant/:participantId/start    # Inicia quiz
POST   /quiz-participation/:quizId/participant/:participantId/finish   # Finaliza quiz
GET    /quiz-participation/:quizId/participant/:participantId/answers  # Obtiene respuestas
GET    /quiz-participation/:quizId/answers                            # Todas las respuestas
```

## 🚀 Instalación y Configuración

1. Clonar el repositorio:
```bash
git clone <repositorio>
cd gateway-api
```

2. Crear entorno virtual:
```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .Template_env .env
# Editar .env con valores correspondientes
```

5. Ejecutar:
```bash
python src/main.py
```

## 🔧 Variables de Entorno

```ini
SECRET_KEY=tu_clave_secreta
JWT_SECRET_KEY=jwt_dev_key

# Servicios
AUTH_HOST=localhost
QA_HOST=localhost
COMPETITION_HOST=localhost

AUTH_PORT=5001
QA_PORT=5003
COMPETITION_PORT=5006

# Configuración
SERVICE_TIMEOUT=5
RETRY_ATTEMPTS=3
LIMITER_DEFAULT_LIMIT=5 per minute
LIMITER_STORAGE_URL=redis://localhost:6379
PORT=5500
```

## 🧪 Pruebas

```bash
pytest tests/
```

## 🔐 Roles y Permisos

- **Admin/Moderator**: Gestión completa de cuestionarios, preguntas y competencias
- **Usuario**: Participación en competencias y acceso a cuestionarios
- **Sin autenticar**: Solo acceso a endpoints públicos

## 🐳 Docker

```bash
# Construir imagen
docker build -t gateway-api .

# Ejecutar contenedor
docker run -p 5000:5000 gateway-api
```

## 📝 Logging

El sistema utiliza logging centralizado para monitorear:
- Errores de autenticación
- Fallos en servicios
- Peticiones rechazadas por rate limiting
- Errores de validación

## 👥 Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -am 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Crear Pull Request