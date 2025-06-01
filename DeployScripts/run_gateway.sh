#!/bin/bash
#
# Script para instalar Docker (si es necesario), hacer login en Docker Hub (si no hay sesión activa),
# descargar la imagen de “enrutador” (metabolite-separation-api) y levantar el contenedor.
# Ahora acepta por parámetros (en orden):
#   1) PREDICTOR_HOST    (por defecto: 192.168.189.168)
#   2) PREDICTOR_PORT    (por defecto: 8000)
#   3) DATABASE_API_HOST (por defecto: 192.168.189.168)
#   4) DATABASE_API_PORT (por defecto: 8010)
#
# Uso:
#   ./run_enrutador.sh [PREDICTOR_HOST] [PREDICTOR_PORT] [DATABASE_API_HOST] [DATABASE_API_PORT]
# Ejemplo:
#   ./run_enrutador.sh 10.0.0.5 9000 10.0.0.5 9200
#

set -euo pipefail

DOCKERHUB_USER="cmoragon"
IMAGE="cmoragon/enrutador:latest"
CONTAINER_NAME="enrutador"
HOST_PORT=8080
CONTAINER_PORT=8080

# Asignar parámetros con valores por defecto
PREDICTOR_HOST="${1:-192.168.189.168}"
PREDICTOR_PORT="${2:-8000}"
DATABASE_API_HOST="${3:-192.168.189.168}"
DATABASE_API_PORT="${4:-8010}"

# Función: Instalar Docker si no está presente
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

# Función: Hacer login en Docker Hub si no hay sesión activa
docker_login_if_needed() {
  if ! docker info 2>/dev/null | grep -qE '^ Username:'; then
    echo "[INFO] No hay sesión activa en Docker Hub. Debes iniciar sesión:"
    docker login -u "$DOCKERHUB_USER"
  else
    echo "[INFO] Ya existe sesión en Docker Hub."
  fi
}

# -------------------- Ejecución principal --------------------

echo "=== run_enrutador.sh START ==="
echo "   Parámetros empleados:"
echo "     • PREDICTOR_HOST    = $PREDICTOR_HOST"
echo "     • PREDICTOR_PORT    = $PREDICTOR_PORT"
echo "     • DATABASE_API_HOST = $DATABASE_API_HOST"
echo "     • DATABASE_API_PORT = $DATABASE_API_PORT"

install_docker_if_missing
docker_login_if_needed

echo "[STEP 1] Haciendo pull de la imagen de Enrutador: $IMAGE"
docker pull "$IMAGE"

# Si ya existe un contenedor con el mismo nombre, lo detenemos y eliminamos
if docker ps -aq --filter "name=^/${CONTAINER_NAME}$" | grep -q .; then
  echo "[STEP 2] Contenedor previo '$CONTAINER_NAME' encontrado. Deteniendo y eliminando..."
  docker rm -f "$CONTAINER_NAME"
fi

echo "[STEP 3] Levantando contenedor '$CONTAINER_NAME'..."
docker run -d \
  --name "$CONTAINER_NAME" \
  -e PREDICTOR_HOST="$PREDICTOR_HOST" \
  -e PREDICTOR_PORT="$PREDICTOR_PORT" \
  -e DATABASE_API_HOST="$DATABASE_API_HOST" \
  -e DATABASE_API_PORT="$DATABASE_API_PORT" \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  "$IMAGE"

echo "[OK] Contenedor '$CONTAINER_NAME' en ejecución (puerto ${HOST_PORT}→${CONTAINER_PORT})."
echo "    Variables de entorno:"
echo "      • PREDICTOR_HOST    = $PREDICTOR_HOST"
echo "      • PREDICTOR_PORT    = $PREDICTOR_PORT"
echo "      • DATABASE_API_HOST = $DATABASE_API_HOST"
echo "      • DATABASE_API_PORT = $DATABASE_API_PORT"
echo "=== run_enrutador.sh END ==="
