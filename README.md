 
# 🚀 **API Gateway para Sistema de Cuestionarios en Microservicios**

## 📚 **Descripción General**
El **API Gateway** es el punto de entrada centralizado para el sistema de cuestionarios en una arquitectura basada en microservicios. Se encarga de manejar la autenticación, autorización, enrutamiento de solicitudes y comunicación segura entre servicios, garantizando eficiencia, seguridad y escalabilidad.

---

## 🛠️ **Tecnologías Utilizadas**
- **Python** (Flask)
- **PyJWT** (Autenticación JWT)
- **Docker** (Contenedorización)
- **Docker Compose** (Orquestación de servicios)
- **YAML** (Configuración de rutas)

---

## 📂 **Estructura del Proyecto**
```
api-gateway/
├── config/
│   ├── config.py           # Configuraciones globales
│   ├── routes.yaml         # Definición de rutas
│   └── security.py         # Validación JWT y Tokens de Servicio
│
├── controllers/
│   ├── auth_controller.py  # Manejo de autenticación
│   ├── user_controller.py  # Controlador para usuarios
│   ├── service_controller.py # Comunicación interna entre servicios
│
├── middlewares/
│   ├── auth_middleware.py  # Middleware para autenticación
│   └── logging_middleware.py # Middleware de logs
│
├── tests/
│   ├── test_routes.py      # Pruebas de rutas
│   ├── test_auth.py        # Pruebas de autenticación
│   └── test_services.py    # Pruebas de comunicación interna
│
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias
├── docker-compose.yml      # Orquestación Docker
└── .env                    # Variables de entorno
```

---

## 🔑 **Autenticación y Autorización**
- **JWT (JSON Web Token):** Autenticación para usuarios externos.
- **Service Token:** Token estático para comunicación segura entre microservicios.
- **Middleware de Seguridad:** Diferencia entre solicitudes de usuarios y servicios.

### 🧠 **Flujo de Autenticación**
1. Las solicitudes de usuarios deben incluir un **Token JWT**.
2. Las solicitudes entre servicios deben usar un **Token de Servicio** en los encabezados.

---

## 📜 **Rutas Principales**
Las rutas están definidas en `routes.yaml`:

- **Autenticación:** `/auth`
- **Usuarios:** `/quiz/public`
- **Servicios Internos:** `/quiz/internal/completed-quizzes`
- **Estadísticas:** `/stats`

---

## 🐳 **Despliegue con Docker Compose**
```bash
docker-compose up --build
```

### 🌍 **Acceder a la API Gateway:**
```
http://localhost:5000/
```

---

## ✅ **Pruebas**
Ejecuta los tests para asegurar la estabilidad del API Gateway:
```bash
pytest tests/
```

---

## 🔄 **Flujo de Comunicación Entre Servicios**
1. Un servicio interno (por ejemplo, **Stats**) solicita información a **Quiz**.
2. El API Gateway valida el **Token de Servicio**.
3. El tráfico se enruta correctamente entre servicios.

---

## 📊 **Variables de Entorno (.env)**
```env
JWT_SECRET_KEY=your_jwt_secret
SERVICE_CLIENT_ID=service_client_id
SERVICE_CLIENT_SECRET=service_client_secret
INTERNAL_SERVICE_TOKEN=service_internal_token
AUTH_SERVICE_URL=http://auth-service
QUIZ_SERVICE_URL=http://quiz-service
STATS_SERVICE_URL=http://stats-service
```

---

## 🤝 **Contribuciones**
¡Las contribuciones son bienvenidas! Si encuentras un problema o deseas mejorar algo, abre un **Issue** o envía un **Pull Request**.

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

```plaintext
Desarrollado con ❤️ por [fom78]
```

