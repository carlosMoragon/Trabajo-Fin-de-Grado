#!/bin/bash

SERVICE_NAME="api-container"
PORT=8080

# Instalar Docker si no está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker no encontrado. Instalando Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    echo "Docker instalado."
fi

# Instalar docker-compose si no está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose no encontrado. Instalando docker-compose..."
    COMPOSE_VERSION="1.29.2"
    curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "docker-compose instalado."
fi

# Cambiar al directorio donde se encuentra el script
cd "$(dirname "$0")"

# Detener y eliminar contenedores que usan el puerto
CONTAINERS=$(docker ps -q -f "publish=$PORT")
if [ -n "$CONTAINERS" ]; then
    echo "Deteniendo contenedores que usan el puerto $PORT..."
    docker stop $CONTAINERS
    echo "Eliminando contenedores..."
    docker rm $CONTAINERS
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
