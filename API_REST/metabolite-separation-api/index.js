const config = require('./config');
const logger = require('./logger');
const ExpressServer = require('./expressServer');
const mongoose = require('mongoose');

const launchServer = async () => {
  try {
    // Conectar a MongoDB (sin opciones deprecadas)
    await mongoose.connect('mongodb://localhost:27017/metabolite-separation-api');
    console.log('✅ MongoDB connected');

    // Iniciar servidor Express
    const expressServer = new ExpressServer(config.URL_PORT, config.OPENAPI_YAML);
    expressServer.launch();
    logger.info('Express server running');
  } catch (error) {
    logger.error('Express Server failure', error.message);
    await mongoose.connection.close();
  }
};

launchServer().catch(e => logger.error(e));


