#!/bin/bash

install_docker() {
    echo "Docker no está instalado. Instalando Docker..."
    
    sudo dnf -y update
    sudo dnf -y install dnf-plugins-core
    sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf -y install docker-ce docker-ce-cli containerd.io
    sudo systemctl start docker
    sudo systemctl enable docker
    # Agregamos el usuario actual al grupo docker
    sudo usermod -aG docker $USER
    echo "Docker instalado exitosamente. Reinicia la sesión para que los cambios tengan efecto."
}

install_docker_compose() {
    echo "Docker Compose no está instalado. Instalando Docker Compose..."

    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    echo "Docker Compose instalado exitosamente."
}

# Verificamos si Docker está instalado
if ! command -v docker &> /dev/null
then
    install_docker
fi

# Verificamos si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null
then
    install_docker_compose
fi

# Levanta el entorno usando Docker Compose
echo "Levantando el entorno con Docker Compose..."
docker-compose up -d 