#!/bin/bash

IMAGE_NAME="metabolite-api"
DOCKERHUB_USERNAME="cmoragon"
DOCKERHUB_REPO="metabolite-separation-api"

cd "$(dirname "$0")"

echo "Iniciando sesión en Docker Hub..."
docker login -u $DOCKERHUB_USERNAME

echo "Etiquetando la imagen..."
docker tag $IMAGE_NAME $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest

echo "Subiendo la imagen a Docker Hub..."
docker push $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest

echo "Imagen subida a Docker Hub: $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest"
