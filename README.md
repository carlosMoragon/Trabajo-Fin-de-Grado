# MetaboPredictor

## Título
**Predicción de configuraciones experimentales en cromatografía líquida para la separación de metabolitos mediante inteligencia artificial**

---

## Autores
- **Carlos Moragón Corella**  
  Autor del proyecto  
- **Alberto Gil de la Fuente**  
  Tutor  
- **Constantino Antonio García Martínez**  
  Co-tutor  

---

## Despliegue del sistema

### 1. Requisitos previos
- Sistema operativo: Amazon Linux 2 / AL2023, CentOS 7/8, RHEL equivalente, Debian > 9 o Ubuntu > 18.03  
- Permisos **root** o **sudo**  
- Conectividad a Internet  
- Cuenta y credenciales en Docker Hub  
- Git instalado  

---

### 2. Desplegar microservicios

#### 2.1 Gateway (enrutador)
1. Clonar o copiar `run_enrutador.sh` al servidor Gateway.  
2. Darle permisos de ejecución:
   ```bash
   chmod +x run_enrutador.sh
   ```
3. Ejecutar con:
  ```bash
  ./run_enrutador.sh [PREDICTOR_HOST] [PREDICTOR_PORT] [DATABASE_API_HOST] [DATABASE_API_PORT]
  ```
  - PREDICTOR_HOST/PORT: dirección y puerto del microservicio de procesamiento.
  - DATABASE_API_HOST/PORT: dirección y puerto del microservicio de persistencia.

### 2.2 Persistencia (API + MongoDB)
1. Clonar o copia `run_persistencia.sh` al servidor de base de datos.
2. Dar permisos:
   ```bash
   chmod +x run_persistencia.sh
   ```
4. Ejecutar con:
   ```bash
   .\run_persistencia.sh
   ```
   Esto levantará:
   - Un contenedor MongoDB con persistencia de datos.
   - Un contenedor API de persistencia (cmoragon/persistencia:latest)

### 2.2 Procesador (predictor)
1. Clonar o copia `run_procesasdor.sh` al servidor de base de datos.
2. Dar permisos:
   ```bash
   chmod +x run_procesasdor.sh
   ```
4. Ejecutar con:
   ```bash
   .\run_persistencia.sh
   ```
   Esto levantará el microservicio (cmoragon/procesador:latest) en el puerto 80.

### 3. Configurar proxy inverso con Nginx y TLS
1. Dejar el Gateway escuchando en el puerto 8080.
2. Instalar y habilitar Nginx:
   ```bash
    yum install -y nginx
    systemctl enable nginx
   ```
4. Instalar Certbot y el plugin Nginx:
   ```bash
    yum install -y epel-release
    yum install -y certbot python3-certbot-nginx
   ```
6. Apuntar el dominio metabopredictor.com (y www.) a la IP pública del servidor vía DNS.
7. Obtener certificados:
   ```bash
   certbot --nginx -d metabopredictor.com -d www.metabopredictor.com
   ```
9. Verificar que en /etc/nginx/conf.d/metabopredictor.com.conf existe un bloque server redirigiendo a http://localhost:8080.
10. Recargar Nginx:
    ```bash
    systemctl reload nginx
    ```
12. Acceder a https://metabopredictor.com/api-docs para comprobar la interfaz Swagger.



