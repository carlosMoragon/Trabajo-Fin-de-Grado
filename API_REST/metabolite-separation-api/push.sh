#!/bin/bash

set -e

IMAGE_NAME="metabolite-api"
DOCKERHUB_USERNAME="cmoragon"
DOCKERHUB_REPO="metabolite-separation-api"

cd "$(dirname "$0")"

echo "[INFO] Iniciando sesión en Docker Hub..."
docker login -u $DOCKERHUB_USERNAME

echo "[INFO] Etiquetando la imagen..."
docker tag $IMAGE_NAME $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest

echo "[INFO] Subiendo la imagen a Docker Hub..."
docker push $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest

echo "[INFO] Imagen subida a Docker Hub: $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest"
