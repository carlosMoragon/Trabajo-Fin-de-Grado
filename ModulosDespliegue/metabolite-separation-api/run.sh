#!/bin/bash

SERVICE_NAME="api-container"
PORT=8080

set -e

install_docker() {
    echo "[INFO] Instalando Docker..."
    sudo dnf -y update
    sudo dnf -y install dnf-plugins-core
    sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf -y install docker-ce docker-ce-cli containerd.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    echo "[INFO] Docker instalado. Reinicia la sesión para aplicar cambios de grupo."
}

install_docker_compose() {
    echo "[INFO] Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "[INFO] Docker Compose instalado."
}

echo "[INFO] Verificando instalación de Docker y Compose..."

if ! command -v docker &> /dev/null; then
    install_docker
fi

if ! command -v docker-compose &> /dev/null; then
    install_docker_compose
fi

# Detener los contenedores que están utilizando el puerto 8080
CONTAINER_ID=$(docker ps -q -f "expose=$PORT")

if [ -n "$CONTAINER_ID" ]; then
    echo "Deteniendo los contenedores que están utilizando el puerto $PORT..."
    docker stop $CONTAINER_ID
else
    echo "No se encontraron contenedores usando el puerto $PORT."
fi

# Levantar el contenedor con docker-compose
echo "Levantando el contenedor con docker-compose..."
docker-compose up --build -d

# Verificar si el contenedor está corriendo
if [ "$(docker ps -q -f name=$SERVICE_NAME)" ]; then
    echo "Contenedor $SERVICE_NAME corriendo en el puerto $PORT"
else
    echo "Hubo un problema al iniciar el contenedor."
    exit 1
fi
