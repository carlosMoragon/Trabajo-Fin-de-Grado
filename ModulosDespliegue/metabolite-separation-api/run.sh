#!/bin/bash

SERVICE_NAME="api-container"
PORT=8080

cd "$(dirname "$0")"

echo "Levantando el contenedor con docker-compose..."
docker-compose up --build -d

if [ "$(docker ps -q -f name=$SERVICE_NAME)" ]; then
    echo "Contenedor $SERVICE_NAME corriendo en el puerto $PORT"
else
    echo "Hubo un problema al iniciar el contenedor."
    exit 1
fi
