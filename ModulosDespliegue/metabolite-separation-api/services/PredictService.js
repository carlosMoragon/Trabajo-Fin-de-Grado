/*const config = require('../config');
const axios = require('axios');
const logger = require('../logger');

const predict = async (req, res) => {
  const { family } = req.body;
  const db_host = config.DATABASE_API_HOST;
  const db_port = config.DATABASE_API_PORT;
  const host = config.PREDICTOR_HOST;
  const port = config.PREDICTOR_PORT;

  if (!family) {
    return res.status(400).json({ error: 'Missing "family" field.' });
  }

  try {
    // 1. Revisar caché (Buscar en la base de datos)

    const cachedLog = await axios.post(`http://${db_host}:${db_port}/predict/cache`, req.body);

    if (cachedLog.data.cached == true) {
      res.locals.responseAlreadySent = true;
      res.locals.calculatedResponse = cachedLog.data;
    
      res.status(200).json(cachedLog.data.result.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en predict:', err);
  }

  try {
    
    // 2. Llamar al servicio externo (en vez del script local)
    const response = await axios.post(`http://${host}:${port}/predict`, { family });

    const result = response.data;

    // 3. Guardar el resultado en la base de datos (caché)
    setImmediate(async () => {
      try {
        await axios.post(`http://${db_host}:${db_port}/predict/save`, {
          API_version: 1,
          request: req.body,
          respond: result,
        });
      } catch (saveErr) {
        logger.error('Error guardando en la caché (predict):', saveErr);
      }
    });
    
    // Enviar la respuesta al cliente
    if (!res.locals.responseAlreadySent) {
      return res.status(200).json(result);
    }
  } catch (error) {
    logger.error('Error al llamar al servicio de predicción externo:', error.message);

    if (error.response) {
      return res.status(error.response.status).json({
        error: 'Error from prediction service',
        details: error.response.data,
      });
    }

    return res.status(500).json({ error: 'Prediction service unavailable' });
  }
};

module.exports = { predict };
*/
const config = require('../config');
const axios = require('axios');
const logger = require('../logger');
const predict = async (req, res) => {
  const { class: metaboliteClass } = req.body;
  const db_host = config.DATABASE_API_HOST;
  const db_port = config.DATABASE_API_PORT;
  const host = config.PREDICTOR_HOST;
  const port = config.PREDICTOR_PORT;

  if (!metaboliteClass) {
    return res.status(400).json({ error: 'Missing "class" field.' });
  }

  const requestPayload = { family: metaboliteClass }; // alias compatible con los microservicios antiguos

  try {
    const cachedLog = await axios.post(`http://${db_host}:${db_port}/predict/cache`, requestPayload);

    if (cachedLog.data.cached === true) {
      res.locals.responseAlreadySent = true;
      res.locals.calculatedResponse = cachedLog.data;
      return res.status(200).json(cachedLog.data.result.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en predict:', err);
  }

  try {
    const response = await axios.post(`http://${host}:${port}/predict`, requestPayload);

    const result = response.data;

    setImmediate(async () => {
      try {
        await axios.post(`http://${db_host}:${db_port}/predict/save`, {
          API_version: 1,
          request: requestPayload,
          respond: result,
        });
      } catch (saveErr) {
        logger.error('Error guardando en la caché (predict):', saveErr);
      }
    });

    if (!res.locals.responseAlreadySent) {
      return res.status(200).json(result);
    }
  } catch (error) {
    logger.error('Error al llamar al servicio de predicción externo:', error.message);

    if (error.response) {
      return res.status(error.response.status).json({
        error: 'Error from prediction service',
        details: error.response.data,
      });
    }

    return res.status(500).json({ error: 'Prediction service unavailable' });
  }
};
module.exports = { predict };