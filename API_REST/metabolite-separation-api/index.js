const config = require('./config');
const logger = require('./logger');
const ExpressServer = require('./expressServer');
const mongoose = require('mongoose');

const launchServer = async () => {
  try {
    require('dotenv').config(); 
    const host = config.HOSTDB;
    const port = config.PORTDB;
    const name = config.NAMEDB;
    const user = config.USERDB;
    const password = config.PASSWORDDB;

    await mongoose.connect(`mongodb://${user}:${password}@${host}:${port}/${name}?authSource=admin`);
    console.log('✅ MongoDB connected');

    const expressServer = new ExpressServer(config.URL_PORT, config.OPENAPI_YAML);
    expressServer.launch();
    logger.info('Express server running');
  } catch (error) {
    logger.error('Express Server failure', error.message, error.stack);
    await mongoose.connection.close();
  }
};

launchServer().catch(e => logger.error(e));
