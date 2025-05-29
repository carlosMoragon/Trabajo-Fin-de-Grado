# deploy_api.sh
#!/bin/bash

set -e

SERVICE_NAME="api-container"
PORT=8080

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
    COMPOSE_VERSION="1.29.2"
    sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
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

# Cambiar al directorio donde se encuentra el script
cd "$(dirname "$0")"

# Detener y eliminar contenedores que usan el puerto

echo "[INFO] Buscando contenedores que exponen el puerto $PORT..."
CONTAINERS=$(docker ps -q -f "publish=$PORT")
if [ -n "$CONTAINERS" ]; then
    echo "[INFO] Deteniendo contenedores en el puerto $PORT..."
    docker stop $CONTAINERS
    echo "[INFO] Eliminando contenedores..."
    docker rm $CONTAINERS
else
    echo "[INFO] No se encontraron contenedores usando el puerto $PORT."
fi

# Detener servicios de docker-compose previos

echo "[INFO] Deteniendo servicios definidos en docker-compose..."

docker-compose down

# Levantar servicios con docker-compose
echo "[INFO] Levantando servicios con Docker Compose..."

docker-compose up -d --build

# Verificar que el servicio esté corriendo
if [ "$(docker ps -q -f name=$SERVICE_NAME)" ]; then
    echo "[INFO] Contenedor $SERVICE_NAME corriendo en el puerto $PORT"
else
    echo "[ERROR] Hubo un problema al iniciar el contenedor $SERVICE_NAME."
    exit 1
fi


# deploy_predictor.sh
#!/bin/bash

set -e

IMAGE_NAME="predictor"
CONTAINER_NAME="predictor-container"
PREDICTOR_PORT=8000

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
    COMPOSE_VERSION="1.29.2"
    sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
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

# Cambiar al directorio donde se encuentra el script
cd "$(dirname "$0")"

# Verificar y liberar el puerto del predictor

echo "[INFO] Buscando contenedores que exponen el puerto $PREDICTOR_PORT..."
P_CONTAINERS=$(docker ps -q -f "publish=$PREDICTOR_PORT")
if [ -n "$P_CONTAINERS" ]; then
    echo "[INFO] Deteniendo contenedores en el puerto $PREDICTOR_PORT..."
    docker stop $P_CONTAINERS
    echo "[INFO] Eliminando contenedores..."
    docker rm $P_CONTAINERS
else
    echo "[INFO] No se encontraron contenedores usando el puerto $PREDICTOR_PORT."
fi

# Construir la imagen Docker
echo "[INFO] Construyendo imagen Docker $IMAGE_NAME..."
docker build -t $IMAGE_NAME .

# Eliminar contenedor anterior si existe
echo "[INFO] Eliminando contenedor anterior si existe..."
if docker ps -aq -f name=$CONTAINER_NAME > /dev/null; then
    docker rm -f $CONTAINER_NAME
fi

# Iniciar el contenedor
echo "[INFO] Iniciando contenedor..."
docker run -d --name $CONTAINER_NAME -p $PREDICTOR_PORT:$PREDICTOR_PORT $IMAGE_NAME

# Mostrar logs del contenedor
echo "[INFO] Mostrando logs del contenedor $CONTAINER_NAME (Ctrl+C para salir):"
docker logs -f $CONTAINER_NAME