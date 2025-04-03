FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Definir el argumento QA_PORT (valor se pasa desde docker-compose)
ARG API_PORT=5500

# Definirlo como variable de entorno
ENV PORT=$API_PORT

CMD ["python", "src/main.py"]
