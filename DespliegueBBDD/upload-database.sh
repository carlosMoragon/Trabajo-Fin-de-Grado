#!/bin/bash

install_docker() {
    echo "Docker no está instalado. Instalando Docker..."
    
    sudo dnf -y update
    sudo dnf -y install dnf-plugins-core
    sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf -y install docker-ce docker-ce-cli containerd.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    echo "Docker instalado exitosamente. Reinicia la sesión para que los cambios tengan efecto."
}

install_docker_compose() {
    echo "Docker Compose no está instalado. Instalando Docker Compose..."

    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    echo "Docker Compose instalado exitosamente."
}

if ! command -v docker &> /dev/null
then
    install_docker
fi

if ! command -v docker-compose &> /dev/null
then
    install_docker_compose
fi

# Variables necesarias para el Docker Hub
DOCKER_USERNAME="cmoragon" 
DOCKER_REPO="metabolite-separation-api"
TAG="latest"

echo "Construyendo la imagen Docker..."
docker build -t $DOCKER_USERNAME/$DOCKER_REPO:$TAG .

echo "Iniciando sesión en Docker Hub..."
docker login -u $DOCKER_USERNAME

echo "Subiendo la imagen a Docker Hub..."
docker push $DOCKER_USERNAME/$DOCKER_REPO:$TAG

echo "La imagen Docker se ha subido exitosamente a Docker Hub."
