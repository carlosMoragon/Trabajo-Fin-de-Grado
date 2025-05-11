#!/bin/bash

set -e

USERNAME="cmoragon"
IMAGE_NAME="predictor"
TAG="latest"
FULL_IMAGE_NAME="$USERNAME/metabolite-separation-api-$IMAGE_NAME:$TAG"

echo "[INFO] Etiquetando la imagen como $FULL_IMAGE_NAME..."
docker tag $IMAGE_NAME $FULL_IMAGE_NAME

echo "[INFO] Verificando login en Docker Hub..."
if ! docker info | grep -q "Username: $USERNAME"; then
    echo "[INFO] Iniciando sesión en Docker Hub..."
    docker login -u "$USERNAME"
fi

echo "[INFO] Subiendo imagen a Docker Hub..."
docker push "$FULL_IMAGE_NAME"

echo "[INFO] Imagen subida correctamente: $FULL_IMAGE_NAME"
