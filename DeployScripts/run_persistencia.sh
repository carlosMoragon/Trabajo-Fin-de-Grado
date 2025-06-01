#!/bin/bash
#
# run_persistencia.sh
#
# • Instala Docker si no está presente.
# • Instala Docker Compose (v1.29.2) si no está presente.
# • Genera/asegura un docker-compose.yml que arranca MongoDB + API (imagen de Docker Hub).
# • Lanza ambos contenedores con docker-compose up -d.
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
    echo "Distribución no soportada automáticamente. Instala Docker manualmente." >&2
    exit 1
  fi

  echo "[INFO] Docker instalado y arrancado correctamente."
}

# -------------- 2. Instalar Docker Compose (v1.29.2) si falta --------------

install_docker_compose_if_missing() {
  if command -v docker-compose &>/dev/null; then
    echo "[INFO] Docker Compose ya está instalado."
    return
  fi

  echo "[INFO] Docker Compose no está instalado. Instalando v1.29.2..."

  # Descarga binario y lo coloca en /usr/local/bin
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose

  # Verificar instalación
  if ! command -v docker-compose &>/dev/null; then
    echo "Falla al instalar docker-compose." >&2
    exit 1
  fi

  echo "[INFO] Docker Compose instalado (versión: $(docker-compose --version))."
}

# -------------- 3. Asegurar que exista el docker-compose.yml --------------

ensure_compose_file() {
  local compose_path="./docker-compose.yml"

  # Si ya existe, no lo sobrescribimos. Si quieres regenéralo manualmente aquí.
  if [[ -f "$compose_path" ]]; then
    echo "[INFO] Ya existe docker-compose.yml. Se utilizará el fichero existente."
    return
  fi

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
      - "80:8010"
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
}

# -------------- 4. Iniciar MongoDB + API con docker-compose --------------

start_compose_services() {
  echo "[INFO] Iniciando servicios con docker-compose..."

  # Primero, detener/limpiar si existiera un proyecto anterior
  sudo docker-compose down -v

  # Ahora levantar en background (detached)
  sudo docker-compose up -d

  echo "[OK] MongoDB y API arrancados. Verifica con 'docker ps'."
}

# --------------  Ejecución principal  --------------
echo "=== run_persistencia.sh START ==="

install_docker_if_missing
install_docker_compose_if_missing
ensure_compose_file
start_compose_services

echo "=== run_persistencia.sh END ==="
