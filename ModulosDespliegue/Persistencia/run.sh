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

# Detener y eliminar contenedores, redes y volúmenes previos si existen
echo "[INFO] Deteniendo y eliminando contenedores existentes..."
docker-compose down

echo "[INFO] Levantando servicios con Docker Compose..."
docker-compose up -d --build
