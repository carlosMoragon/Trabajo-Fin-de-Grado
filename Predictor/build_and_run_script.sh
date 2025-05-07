#!/bin/bash

IMAGE_NAME="predictor"
CONTAINER_NAME="predictor-container"

echo "🔧 Construyendo la imagen Docker..."
docker build -t $IMAGE_NAME .

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🧹 Eliminando contenedor anterior..."
    docker rm -f $CONTAINER_NAME
fi

echo "🚀 Iniciando el contenedor..."
docker run -d --name $CONTAINER_NAME -p 8000:8000 $IMAGE_NAME

echo "📋 Mostrando logs (Ctrl+C para salir)..."
docker logs -f $CONTAINER_NAME
