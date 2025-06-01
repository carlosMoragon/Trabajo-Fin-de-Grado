#!/bin/bash
set -euo pipefail

DOCKERHUB_USER="cmoragon"
IMAGE="cmoragon/persistencia:latest"
CONTAINER_NAME="persistencia-api"
HOST_PORT=8010
CONTAINER_PORT=8010

install_docker_if_missing() {
  if command -v docker &>/dev/null; then
    echo "[INFO] Docker ya estaba instalado."
    return
  fi

  echo "[INFO] Docker no está instalado. Procediendo a instalarlo..."

  # Detectar Amazon Linux 2023
  if grep -qi "amazon linux.*2023" /etc/os-release; then
    echo "[INFO] Distribución detectada: Amazon Linux 2023"
    dnf update -y
    dnf install -y docker
    systemctl enable docker
    systemctl start docker

  else
    echo "Distribución no soportada automáticamente. Instala Docker manualmente." >&2
    exit 1
  fi

  echo "[INFO] Docker instalado y arrancado correctamente."
}

docker_login_if_needed() {
  if ! docker info 2>/dev/null | grep -qE '^ Username:'; then
    echo "[INFO] No hay sesión activa en Docker Hub. Debes iniciar sesión:"
    docker login -u "$DOCKERHUB_USER"
  else
    echo "[INFO] Ya existe sesión en Docker Hub."
  fi
}

echo "=== run_persistencia.sh START ==="
install_docker_if_missing
docker_login_if_needed

echo "[STEP 1] Haciendo pull de la imagen de Persistencia: $IMAGE"
docker pull "$IMAGE"

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
