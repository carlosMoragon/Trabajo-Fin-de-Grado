#!/bin/bash

set -e

IMAGE_NAME="metabolite-api"
CONTAINER_NAME="api-container"
PORT=8080

cd "$(dirname "$0")"

echo "[INFO] Construyendo la imagen Docker..."
docker build -t $IMAGE_NAME .

# Detener y eliminar el contenedor anterior si ya existe
echo "[INFO] Deteniendo y eliminando contenedor si existe..."
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

# Iniciar el nuevo contenedor
echo "[INFO] Ejecutando el contenedor..."
docker run -d --name $CONTAINER_NAME -p $PORT:$PORT --restart always $IMAGE_NAME

echo "[INFO] Contenedor $CONTAINER_NAME corriendo en el puerto $PORT"
