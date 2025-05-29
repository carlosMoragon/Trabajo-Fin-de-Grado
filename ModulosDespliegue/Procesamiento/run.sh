#!/bin/bash

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

IMAGE_NAME="predictor"
CONTAINER_NAME="predictor-container"

echo "[INFO] Construyendo imagen Docker..."
docker build -t $IMAGE_NAME .

if docker ps -aq -f name=$CONTAINER_NAME > /dev/null; then
    echo "[INFO] Eliminando contenedor anterior..."
    docker rm -f $CONTAINER_NAME
fi

echo "[INFO] Iniciando contenedor..."
docker run -d --name $CONTAINER_NAME -p 8000:8000 $IMAGE_NAME

echo "[INFO] Logs del contenedor (Ctrl+C para salir):"
docker logs -f $CONTAINER_NAME
