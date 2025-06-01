#!/bin/bash
#
# run_persistencia.sh
#
# • Instala Docker si no está presente.
# • Instala el paquete libxcrypt-compat para que docker-compose standalone funcione.
# • Instala Docker Compose v1.29.2 si no está presente.
# • Genera docker-compose.yml para MongoDB + API (imagen de Docker Hub).
# • Lanza ambos servicios con docker-compose up -d.
#
# Uso:
#   cd DeployScripts
#   chmod +x run_persistencia.sh
#   ./run_persistencia.sh
#

set -euo pipefail

DOCKERHUB_USER="cmoragon"
API_IMAGE="cmoragon/persistencia:latest"

# -------------- 1. Instalar Docker si falta --------------

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

  else
    echo "❌ Distribución no soportada automáticamente. Instala Docker manualmente." >&2
    exit 1
  fi

  echo "[INFO] Docker instalado y arrancado correctamente."
}

# -------------- 2. Instalar libxcrypt-compat si falta --------------

install_libcrypt_compat() {
  if ldconfig -p | grep -q "libcrypt.so.1"; then
    echo "[INFO] libcrypt.so.1 ya está presente."
    return
  fi

  echo "[INFO] Instalando libxcrypt-compat para compatibilidad con docker-compose..."
  # En Amazon Linux 2023, este paquete proporciona libcrypt.so.1
  dnf install -y libxcrypt-compat
  echo "[INFO] libxcrypt-compat instalado."
}

# -------------- 3. Instalar Docker Compose v1.29.2 si falta --------------

install_docker_compose_if_missing() {
  if command -v docker-compose &>/dev/null; then
    echo "[INFO] Docker Compose ya está instalado."
    return
  fi

  echo "[INFO] Docker Compose no está instalado. Instalando v1.29.2..."

  # Descarga binario
  curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose

  # Verificar que ya existe la librería libcrypt.so.1, requerido arriba.
  if ! command -v docker-compose &>/dev/null; then
    echo "❌ Falla al instalar docker-compose." >&2
    exit 1
  fi

  echo "[INFO] Docker Compose instalado (versión: $(docker-compose --version))."
}

# -------------- 4. Asegurar que exista el docker-compose.yml --------------

ensure_compose_file() {
  local compose_path="./docker-compose.yml"

  # Si no existe, lo crea
  if [[ ! -f "$compose_path" ]]; then
    echo "[INFO] Creando docker-compose.yml para MongoDB + API..."
    cat > "$compose_path" << 'EOF'
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: mongo-container
    ports:
      - "127.0.0.1:27017:27017"
    volumes:
      - mongodb_data:/data/db
      - ./mongo-init:/docker-entrypoint-initdb.d:ro
    networks:
      - app-network
    restart: always

  api:
    image: cmoragon/persistencia:latest
    container_name: persistencia-api
    depends_on:
      - mongodb
    ports:
      - "8010:8010"
    networks:
      - app-network
    environment:
      - MONGO_URI=mongodb://mongodb:27017
    restart: always

volumes:
  mongodb_data:
    driver: local

networks:
  app-network:
    driver: bridge
EOF
    echo "[INFO] docker-compose.yml creado."
  else
    echo "[INFO] Ya existe docker-compose.yml. Se usará el existente."
  fi
}

# -------------- 5. Iniciar MongoDB + API con docker-compose --------------

start_compose_services() {
  echo "[INFO] Iniciando servicios con docker-compose…"

  # Detener y limpiar cualquier stack anterior (incluye volúmenes anónimos)
  docker-compose down -v

  # Levantar en modo “detached”
  docker-compose up -d

  echo "[OK] MongoDB y API arrancados. Verifica con 'docker ps'."
}

# --------------  Ejecución principal  --------------
echo "=== run_persistencia.sh START ==="

install_docker_if_missing
install_libcrypt_compat
install_docker_compose_if_missing
ensure_compose_file
start_compose_services

echo "=== run_persistencia.sh END ==="
