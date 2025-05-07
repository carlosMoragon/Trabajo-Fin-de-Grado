#!/bin/bash

set -e  # Salir si ocurre algún error

echo "Verificando instalación de Docker..."

if ! command -v docker &> /dev/null; then
  echo "🚧 Docker no está instalado. Instalando Docker..."
  sudo dnf -y update
  sudo dnf -y install dnf-plugins-core
  sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  sudo dnf -y install docker-ce docker-ce-cli containerd.io
  sudo systemctl start docker
  sudo systemctl enable docker
  sudo usermod -aG docker $USER
  echo "Docker instalado. Reinicia sesión si es necesario para aplicar permisos de grupo."
else
  echo "Docker ya está instalado."
fi

echo "Verificando instalación de Docker Compose..."

if ! command -v docker-compose &> /dev/null; then
  echo "🚧 Instalando Docker Compose..."
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
       -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  echo "Docker Compose instalado."
else
  echo "Docker Compose ya está instalado."
fi

echo "Limpiando contenedores existentes si es necesario..."
docker rm -f mongo-container predictor api-container 2>/dev/null || true

echo "Ejecutando orquestación con Docker Compose..."
docker-compose up --build -d

echo "Servicios desplegados correctamente."
