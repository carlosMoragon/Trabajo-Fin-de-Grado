#!/bin/bash

IMAGE="cmoragon/persistencia:latest"
CONTAINER_NAME="persistencia-api"
PORT=8010

echo "[INFO] Verificando si Docker está instalado..."
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker no está instalado. Instálalo y vuelve a intentarlo."
    exit 1
fi

echo "[INFO] Descargando imagen $IMAGE..."
docker pull $IMAGE

echo "[INFO] Eliminando contenedor anterior (si existe)..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

echo "[INFO] Ejecutando contenedor $CONTAINER_NAME..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $PORT:8010 \
  -e MONGO_URI=mongodb://localhost:27017 \
  $IMAGE

echo "[INFO] Contenedor $CONTAINER_NAME desplegado en el puerto $PORT."
