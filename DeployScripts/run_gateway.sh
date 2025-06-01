#!/bin/bash
#
# Script corregido para Amazon Linux 2 / Amazon Linux 2023 / CentOS / RHEL:
#   • Instala Docker usando el paquete "docker" en lugar de "docker-ce" en Amazon Linux 2023.
#   • Hace login en Docker Hub si no hay sesión activa.
#   • Descarga la imagen de “enrutador” y arranca el contenedor con variables por parámetro.
#
# Uso:
#   ./run_enrutador.sh [PREDICTOR_HOST] [PREDICTOR_PORT] [DATABASE_API_HOST] [DATABASE_API_PORT]
#

set -euo pipefail

DOCKERHUB_USER="cmoragon"
IMAGE="cmoragon/enrutador:latest"
CONTAINER_NAME="enrutador"
HOST_PORT=8080
CONTAINER_PORT=8080

# Parámetros con valores por defecto
PREDICTOR_HOST="${1:-192.168.189.168}"
PREDICTOR_PORT="${2:-8000}"
DATABASE_API_HOST="${3:-192.168.189.168}"
DATABASE_API_PORT="${4:-8010}"

# Detectar distro para elegir instalación de Docker
install_docker_if_missing() {
  if command -v docker &>/dev/null; then
    echo "[INFO] Docker ya estaba instalado."
    return
  fi

  echo "[INFO] Docker no está instalado. Procediendo a instalarlo..."

  # Detectar Amazon Linux 2023 / 2 / CentOS / RHEL
  if grep -qiE "amazon linux.*2023" /etc/os-release; then
    echo "[INFO] Detección: Amazon Linux 2023"
    # En AL2023, el paquete se llama "docker"
    dnf update -y
    dnf install -y docker
    systemctl enable docker
    systemctl start docker

  elif grep -qiE "amazon linux.*2" /etc/os-release; then
    echo "[INFO] Detección: Amazon Linux 2"
    # Amazon Linux 2 usa yum + amazon-linux-extras
    yum update -y
    amazon-linux-extras enable docker
    yum install -y docker
    systemctl enable docker
    systemctl start docker

  elif command -v yum &>/dev/null; then
    # CentOS / RHEL 7 o 8
    echo "[INFO] Detección: CentOS/RHEL"
    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    yum install -y docker-ce docker-ce-cli containerd.io
    systemctl enable docker
    systemctl start docker

  elif command -v apt-get &>/dev/null; then
    # Ubuntu / Debian
    echo "[INFO] Detección: Debian/Ubuntu"
    apt-get update
    apt-get install -y docker.io
    systemctl enable docker
    systemctl start docker

  else
    echo "No se reconoce el gestor de paquetes. Instala Docker manualmente." >&2
    exit 1
  fi

  echo "[INFO] Docker instalado y arrancado correctamente."
}

# Login en Docker Hub si no hay sesión activa
docker_login_if_needed() {
  if ! docker info 2>/dev/null | grep -qE '^ Username:'; then
    echo "[INFO] No hay sesión activa en Docker Hub. Debes iniciar sesión ahora:"
    docker login -u "$DOCKERHUB_USER"
  else
    echo "[INFO] Ya existe sesión en Docker Hub."
  fi
}

# ---------- Ejecución principal ----------

echo "=== run_enrutador.sh START ==="
echo "  Parámetros empleados:"
echo "    • PREDICTOR_HOST    = $PREDICTOR_HOST"
echo "    • PREDICTOR_PORT    = $PREDICTOR_PORT"
echo "    • DATABASE_API_HOST = $DATABASE_API_HOST"
echo "    • DATABASE_API_PORT = $DATABASE_API_PORT"

install_docker_if_missing
docker_login_if_needed

echo "[STEP 1] Haciendo pull de la imagen de Enrutador: $IMAGE"
docker pull "$IMAGE"

# Si existe un contenedor previo, lo detenemos y eliminamos
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
echo "      • PREDICTOR_HOST=$PREDICTOR_HOST"
echo "      • PREDICTOR_PORT=$PREDICTOR_PORT"
echo "      • DATABASE_API_HOST=$DATABASE_API_HOST"
echo "      • DATABASE_API_PORT=$DATABASE_API_PORT"
echo "=== run_enrutador.sh END ==="
