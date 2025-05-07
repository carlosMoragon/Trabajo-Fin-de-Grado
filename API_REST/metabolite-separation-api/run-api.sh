#!/bin/bash

IMAGE_NAME="metabolite-api"
CONTAINER_NAME="api-container"
PORT=8080

cd "$(dirname "$0")"

echo "Construyendo la imagen Docker..."
docker build -t $IMAGE_NAME .

echo "Deteniendo y eliminando contenedor si ya existe..."
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

echo "Ejecutando el contenedor..."
docker run -d --name $CONTAINER_NAME -p $PORT:$PORT --restart always $IMAGE_NAME

echo "Contenedor $CONTAINER_NAME corriendo en el puerto $PORT"
