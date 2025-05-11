const path = require('path');

const config = {
  ROOT_DIR: __dirname,
  URL_PORT: 8080,
  URL_PATH: 'http://localhost',
  BASE_VERSION: '',
  CONTROLLER_DIRECTORY: path.join(__dirname, 'controllers'),
  PROJECT_DIR: __dirname,
  // Aquí accedemos directamente a las variables de entorno que Docker ha inyectado
  PREDICTOR_HOST: process.env.PREDICTOR_HOST || 'predictor',
  PREDICTOR_PORT: process.env.PREDICTOR_PORT || 8000,
  DATABASE_API_HOST: process.env.DATABASE_API_HOST || 'localhost',
  DATABASE_API_PORT: process.env.DATABASE_API_PORT || 8010
};

config.OPENAPI_YAML = path.join(config.ROOT_DIR, 'api', 'openapi.yaml');
config.FULL_PATH = `${config.URL_PATH}:${config.URL_PORT}/${config.BASE_VERSION}`;
config.FILE_UPLOAD_PATH = path.join(config.PROJECT_DIR, 'uploaded_files');

module.exports = config;
