#!/bin/bash

SERVICE_NAME="api-container"
PORT=8080

# Cambiar al directorio donde se encuentra el script
cd "$(dirname "$0")"

# Detener los contenedores que están utilizando el puerto 8080
CONTAINER_ID=$(docker ps -q -f "expose=$PORT")

if [ -n "$CONTAINER_ID" ]; then
    echo "Deteniendo los contenedores que están utilizando el puerto $PORT..."
    docker stop $CONTAINER_ID
else
    echo "No se encontraron contenedores usando el puerto $PORT."
fi

# Levantar el contenedor con docker-compose
echo "Levantando el contenedor con docker-compose..."
docker-compose up --build -d

# Verificar si el contenedor está corriendo
if [ "$(docker ps -q -f name=$SERVICE_NAME)" ]; then
    echo "Contenedor $SERVICE_NAME corriendo en el puerto $PORT"
else
    echo "Hubo un problema al iniciar el contenedor."
    exit 1
fi
