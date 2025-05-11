#!/bin/bash

set -e

IMAGE_NAME="predictor"
CONTAINER_NAME="predictor-container"

echo "[INFO] Construyendo imagen Docker..."
docker build -t $IMAGE_NAME .

if docker ps -aq -f name=$CONTAINER_NAME > /dev/null; then
    echo "[INFO] Eliminando contenedor anterior..."
    docker rm -f $CONTAINER_NAME
fi

echo "[INFO] Iniciando contenedor..."
docker run -d --name $CONTAINER_NAME -p 8000:8000 $IMAGE_NAME

echo "[INFO] Logs del contenedor (Ctrl+C para salir):"
docker logs -f $CONTAINER_NAME
