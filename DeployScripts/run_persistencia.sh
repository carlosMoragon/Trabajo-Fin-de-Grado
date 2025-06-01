#!/bin/bash
#
# Script para instalar Docker (si es necesario), hacer login en Docker Hub (si no hay sesión activa),
# descargar la imagen de persistencia y levantar el contenedor.
#

set -euo pipefail

DOCKERHUB_USER="cmoragon"
IMAGE="cmoragon/persistencia:latest"
CONTAINER_NAME="persistencia-api"
HOST_PORT=8010
CONTAINER_PORT=8010

# ------------- Función: Instalar Docker si no está presente -------------

install_docker_if_missing() {
  if ! command -v docker &>/dev/null; then
    echo "[INFO] Docker no está instalado. Procediendo a instalarlo..."

    if command -v apt-get &>/dev/null; then
      echo "[INFO] Detectado apt-get. Instalando Docker con apt-get..."
      apt-get update
      apt-get install -y docker.io
      systemctl enable docker
      systemctl start docker

    elif command -v yum &>/dev/null; then
      echo "[INFO] Detectado yum. Instalando Docker con yum..."
      yum install -y yum-utils device-mapper-persistent-data lvm2
      yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
      yum install -y docker-ce docker-ce-cli containerd.io
      systemctl enable docker
      systemctl start docker

    else
      echo "No se reconoce el gestor de paquetes (ni apt-get ni yum). Instala Docker manualmente." >&2
      exit 1
    fi

    echo "[INFO] Docker instalado correctamente."
  else
    echo "[INFO] Docker ya estaba instalado."
  fi
}

# ------------- Función: Hacer login en Docker Hub si no hay sesión activa -------------

docker_login_if_needed() {
  # "docker info" muestra "Username: <usuario>" si ya hay login
  if ! docker info 2>/dev/null | grep -qE '^ Username:'; then
    echo "[INFO] No hay sesión activa en Docker Hub. Debes iniciar sesión:"
    docker login -u "$DOCKERHUB_USER"
  else
    echo "[INFO] Ya existe sesión en Docker Hub."
  fi
}

# -------------------- Ejecución principal --------------------

echo "=== run_persistencia.sh START ==="

install_docker_if_missing
docker_login_if_needed

echo "[STEP 1] Haciendo pull de la imagen de Persistencia: $IMAGE"
docker pull "$IMAGE"

#  Si existe un contenedor con el mismo nombre, lo detenemos y eliminamos
if docker ps -aq --filter "name=^/${CONTAINER_NAME}$" | grep -q .; then
  echo "[STEP 2] Contenedor previo '$CONTAINER_NAME' encontrado. Deteniendo y eliminando..."
  docker rm -f "$CONTAINER_NAME"
fi

echo "[STEP 3] Levantando contenedor '$CONTAINER_NAME'..."
docker run -d \
  --name "$CONTAINER_NAME" \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  "$IMAGE"

echo "[OK] Contenedor '$CONTAINER_NAME' en ejecución (puerto ${HOST_PORT}→${CONTAINER_PORT})."
echo "=== run_persistencia.sh END ==="
