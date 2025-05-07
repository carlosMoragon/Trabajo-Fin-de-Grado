#!/bin/bash

USERNAME="cmoragon"
IMAGE_NAME="predictor"
TAG="latest"

# Nombre completo de la imagen
FULL_IMAGE_NAME="$USERNAME/metabolite-separation-api-$IMAGE_NAME:$TAG"

echo "📤 Subiendo la imagen $FULL_IMAGE_NAME a Docker Hub..."

# Subir la imagen ya construida a Docker Hub
docker push $FULL_IMAGE_NAME

# Verificar si la subida fue exitosa
if [ $? -ne 0 ]; then
    echo "❌ Error al subir la imagen. Asegúrate de estar logueado con 'docker login'."
    exit 1
fi

echo "✅ Imagen $FULL_IMAGE_NAME subida correctamente a Docker Hub."
