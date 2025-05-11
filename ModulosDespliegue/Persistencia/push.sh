#!/bin/bash

set -e

DOCKER_USERNAME="cmoragon"
DOCKER_REPO="metabolite-separation-api"
TAG="latest"

IMAGE_NAME="$DOCKER_USERNAME/$DOCKER_REPO:$TAG"

echo "[INFO] Autenticando en Docker Hub..."
docker login -u "$DOCKER_USERNAME"

echo "[INFO] Construyendo la imagen Docker..."
docker build -t "$IMAGE_NAME" ./api

echo "[INFO] Subiendo la imagen a Docker Hub..."
docker push "$IMAGE_NAME"

echo "[INFO] Imagen $IMAGE_NAME subida exitosamente."
