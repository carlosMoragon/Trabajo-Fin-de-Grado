const path = require('path');
//require('dotenv').config(); 
require('dotenv').config({ path: path.resolve(__dirname, '..', '.env') });

const config = {
  ROOT_DIR: __dirname,
  URL_PORT: 8080,
  URL_PATH: 'http://localhost',
  BASE_VERSION: '',
  CONTROLLER_DIRECTORY: path.join(__dirname, 'controllers'),
  PROJECT_DIR: __dirname,
  HOSTDB: process.env.DATABASE_HOST || 'localhost',
  PORTDB: process.env.DATABASE_PORT || 27017,
  NAMEDB: process.env.DATABASE_NAME || 'metabolite-separation-api',
  USERDB: process.env.DATABASE_USER || 'root',
  PASSWORDDB: process.env.DATABASE_PASSWORD || 'rootpassword',
  PREDICTOR_HOST: process.env.PREDICTOR_HOST || 'localhost',
  PREDICTOR_PORT: process.env.PREDICTOR_PORT || 8000
};
config.OPENAPI_YAML = path.join(config.ROOT_DIR, 'api', 'openapi.yaml');
config.FULL_PATH = `${config.URL_PATH}:${config.URL_PORT}/${config.BASE_VERSION}`;
config.FILE_UPLOAD_PATH = path.join(config.PROJECT_DIR, 'uploaded_files');

module.exports = config;
