#!/bin/bash

set -e

SERVICE_NAME="api-container"
PORT=8080
COMPOSE_VERSION="1.29.2"

install_docker() {
    echo "[INFO] Instalando Docker..."
    # Detectar distribución
    if [ -f /etc/os-release ]; then
        . /etc/os-release
    fi
    # Configurar repositorio
    echo "[INFO] Configurando repositorio Docker para ${NAME}..."
    sudo dnf -y install yum-utils
    sudo yum-config-manager \
        --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    # Instalar paquetes
    sudo dnf -y install docker-ce docker-ce-cli containerd.io
    # Iniciar y habilitar servicio
    sudo systemctl enable --now docker
    # Agregar usuario al grupo docker
    sudo usermod -aG docker $USER || true
    echo "[INFO] Docker instalado. Puede que necesites cerrar sesión para aplicar permisos de Docker."
}

install_docker_compose() {
    echo "[INFO] Instalando Docker Compose ${COMPOSE_VERSION}..."
    sudo curl -sSL \
        "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "[INFO] Docker Compose instalado."
}

echo "[INFO] Verificando instalación de Docker y Docker Compose..."

if ! command -v docker &> /dev/null; then
    install_docker
else
    echo "[INFO] Docker ya está instalado."
fi

if ! command -v docker-compose &> /dev/null; then
    install_docker_compose
else
    echo "[INFO] Docker Compose ya está instalado."
fi

# Cambiar al directorio donde se encuentra el script
cd "$(dirname "$0")"

# Comprobar servicio Docker
if ! sudo docker version &> /dev/null; then
    echo "[ERROR] Docker no está corriendo o no se puede acceder. Asegúrate de que el servicio esté iniciado y tu usuario tenga permisos."
    exit 1
fi

# Detener y eliminar contenedores que usan el puerto especificado
echo "[INFO] Buscando contenedores que exponen el puerto $PORT..."
CONTAINERS=$(sudo docker ps -q -f "publish=$PORT")
if [ -n "$CONTAINERS" ]; then
    echo "[INFO] Deteniendo contenedores en el puerto $PORT..."
    sudo docker stop $CONTAINERS
    echo "[INFO] Eliminando contenedores..."
    sudo docker rm $CONTAINERS
else
    echo "[INFO] No se encontraron contenedores usando el puerto $PORT."
fi

# Detener servicios definidos en docker-compose
if [ -f docker-compose.yml ]; then
    echo "[INFO] Deteniendo servicios de docker-compose..."
    sudo docker-compose down
fi

# Levantar servicios
if [ -f docker-compose.yml ]; then
    echo "[INFO] Levantando servicios con Docker Compose..."
    sudo docker-compose up -d --build
else
    echo "[ERROR] No se encontró docker-compose.yml en el directorio $(pwd)."
    exit 1
fi

# Verificar que el contenedor esté corriendo
if sudo docker ps -q -f name=$SERVICE_NAME &> /dev/null; then
    echo "[INFO] Contenedor '$SERVICE_NAME' corriendo en el puerto $PORT"
else
    echo "[ERROR] Hubo un problema al iniciar el contenedor '$SERVICE_NAME'."
    exit 1
fi
