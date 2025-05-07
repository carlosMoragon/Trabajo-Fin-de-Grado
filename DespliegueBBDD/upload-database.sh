#!/bin/bash

DOCKER_USERNAME="cmoragon"
DOCKER_REPO="metabolite-separation-api"
TAG="latest"

echo "Iniciando sesión en Docker Hub..."
docker login -u $DOCKER_USERNAME

echo "Subiendo la imagen a Docker Hub..."
docker push $DOCKER_USERNAME/$DOCKER_REPO:$TAG

echo "La imagen Docker se ha subido exitosamente a Docker Hub."
