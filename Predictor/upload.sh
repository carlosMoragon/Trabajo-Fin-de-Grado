#!/bin/bash

USERNAME="cmoragon"
IMAGE_NAME="predictor"
TAG="latest"

FULL_IMAGE_NAME="$USERNAME/$IMAGE_NAME:$TAG"

echo "🔨 Construyendo la imagen Docker: $FULL_IMAGE_NAME"
docker build -t $FULL_IMAGE_NAME .

if [ $? -ne 0 ]; then
    echo "❌ Error al construir la imagen. Abortando."
    exit 1
fi

echo "📤 Subiendo la imagen a Docker Hub..."
docker push $FULL_IMAGE_NAME

if [ $? -ne 0 ]; then
    echo "❌ Error al subir la imagen. Asegúrate de estar logueado con 'docker login'."
    exit 1
fi

echo "✅ Imagen $FULL_IMAGE_NAME subida correctamente a Docker Hub."
