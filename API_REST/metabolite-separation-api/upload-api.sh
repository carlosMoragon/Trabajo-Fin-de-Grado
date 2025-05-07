#!/bin/bash

# Define el nombre de la imagen y el repositorio en Docker Hub
IMAGE_NAME="metabolite-api"
DOCKERHUB_USERNAME="cmoragon"
DOCKERHUB_REPO="metabolite-separation-api"

# Asegúrate de estar en el directorio correcto (donde está el Dockerfile)
cd "$(dirname "$0")"

# Iniciar sesión en Docker Hub (si no has iniciado sesión previamente)
echo "Iniciando sesión en Docker Hub..."
docker login -u $DOCKERHUB_USERNAME

# Etiquetar la imagen con el repositorio de Docker Hub
echo "Etiquetando la imagen..."
docker tag $IMAGE_NAME $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest

# Subir la imagen a Docker Hub
echo "Subiendo la imagen a Docker Hub..."
docker push $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest

echo "Imagen subida a Docker Hub: $DOCKERHUB_USERNAME/$DOCKERHUB_REPO:latest"
