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

  const requestPayload = { class: metaboliteClass };

  try {
    const famResp = await axios.get(`http://${db_host}:${db_port}/families`);
    // famResp.data puede ser { families: [...] } o directamente un array [...]
    const raw     = famResp.data;
    const families = Array.isArray(raw)
      ? raw
      : Array.isArray(raw.families)
        ? raw.families
        : [];
  
    console.log(
      'Clases disponibles:',
      families.map(entry => entry.class),
      '– buscando:',
      metaboliteClass
    );
  
    const exists = families.some(entry => entry.class === metaboliteClass);
  
    if (!exists) {
      return res
        .status(404)
        .json({ error: `Class "${metaboliteClass}" not found in families.` });
    }
  } catch (err) {
    logger.error('Error fetching families from persistencia:', err);
    return res
      .status(500)
      .json({ error: 'Unable to verify class existence.' });
  }
  
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