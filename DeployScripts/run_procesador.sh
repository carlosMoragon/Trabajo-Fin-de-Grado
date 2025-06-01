#!/bin/bash
#
# run_procesador.sh
#
# • Instala Docker en Amazon Linux 2023 / Amazon Linux 2 / CentOS / Ubuntu si no está presente.
# • Hace login en Docker Hub (si no hay sesión activa).
# • Descarga la imagen “cmoragon/procesador:latest” y arranca el contenedor “predictor”.
#
# Uso:
#   ./run_procesador.sh
#

set -euo pipefail

DOCKERHUB_USER="cmoragon"
IMAGE="cmoragon/procesador:latest"
CONTAINER_NAME="predictor"
HOST_PORT=8000
CONTAINER_PORT=8000

install_docker_if_missing() {
  if command -v docker &>/dev/null; then
    echo "[INFO] Docker ya está instalado."
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

  # Detectar Amazon Linux 2
  elif grep -qi "amazon linux.*2" /etc/os-release; then
    echo "[INFO] Distribución detectada: Amazon Linux 2"
    yum update -y
    amazon-linux-extras enable docker
    yum install -y docker
    systemctl enable docker
    systemctl start docker

  # CentOS / RHEL (7/8)
  elif grep -qiE "centos|rhel" /etc/os-release; then
    echo "[INFO] Distribución detectada: CentOS/RHEL"
    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    yum install -y docker-ce docker-ce-cli containerd.io
    systemctl enable docker
    systemctl start docker

  # Debian / Ubuntu
  elif grep -qiE "ubuntu|debian" /etc/os-release; then
    echo "[INFO] Distribución detectada: Debian/Ubuntu"
    apt-get update
    apt-get install -y docker.io
    systemctl enable docker
    systemctl start docker

  else
    echo "Distribución no soportada automáticamente. Instala Docker manualmente." >&2
    exit 1
  fi

  echo "[INFO] Docker instalado y arrancado correctamente."
}

docker_login_if_needed() {
  # Si no hay un Username en 'docker info', pide login
  if ! docker info 2>/dev/null | grep -qE '^ Username:'; then
    echo "[INFO] No hay sesión activa en Docker Hub. Por favor, inicia sesión:"
    docker login -u "$DOCKERHUB_USER"
  else
    echo "[INFO] Ya existe sesión en Docker Hub."
  fi
}

# ------ Ejecución principal ------
echo "=== run_procesador.sh START ==="

install_docker_if_missing
docker_login_if_needed

echo "[STEP 1] Haciendo pull de la imagen de Predictor: $IMAGE"
docker pull "$IMAGE"

# Si ya existe un contenedor con el mismo nombre, lo detenemos y eliminamos
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
echo "=== run_procesador.sh END ==="
