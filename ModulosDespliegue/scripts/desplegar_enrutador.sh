#!/bin/bash

IMAGE="cmoragon/enrutador:latest"
CONTAINER_NAME="api-container"
PORT=8080

# Cambia estas variables según tus IPs reales
PREDICTOR_HOST="192.168.189.170"
PREDICTOR_PORT="8000"
DATABASE_API_HOST="192.168.189.169"
DATABASE_API_PORT="8010"

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
  -p $PORT:8080 \
  -e PREDICTOR_HOST=$PREDICTOR_HOST \
  -e PREDICTOR_PORT=$PREDICTOR_PORT \
  -e DATABASE_API_HOST=$DATABASE_API_HOST \
  -e DATABASE_API_PORT=$DATABASE_API_PORT \
  $IMAGE

echo "[INFO] Contenedor $CONTAINER_NAME desplegado en el puerto $PORT."
