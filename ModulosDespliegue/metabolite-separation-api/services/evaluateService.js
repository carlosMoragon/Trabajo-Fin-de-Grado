const config = require('../config');
const axios = require('axios');
const logger = require('../logger');

const evaluate = async (req, res) => {
  const body = req.body;
  const db_host = config.DATABASE_API_HOST;
  const db_port = config.DATABASE_API_PORT;
  const host = config.PREDICTOR_HOST;
  const port = config.PREDICTOR_PORT;

  if (!body || typeof body.configuration !== 'object') {
    return res.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  try {
    // 1. Revisar caché
    //const cachedResult = await Evaluate.findOne({ request: req.body }).sort({ 'respond.Score': -1 }).exec();

    const cachedResult = await axios.post(`http://${db_host}:${db_port}/evaluate/cache`, req.body);

    if (cachedResult.data.cached == true) {
      return res.status(200).json(cachedResult.data);
    }

    /*if (cachedResult) {
      cachedResult.cacheHits += 1;
      await cachedResult.save();
      return res.status(200).json(cachedResult.respond);
    }*/
  } catch (err) {
    logger.error('Error al consultar la caché en evaluate:', err);
  }

  try {
    // 2. Llamar al servicio externo /evaluate


    const response = await axios.post(`http://${host}:${port}/evaluate`, body);
    const result = response.data;

    // 3. Guardar resultado en caché
    setImmediate(async () => {
      try {
        await axios.post(`http://${db_host}:${db_port}/evaluate/save`, {
          API_version: 1,
          request: req.body,
          respond: result,
        });
      } catch (saveErr) {
        logger.error('Error guardando en la caché de evaluate:', saveErr);
      }
    });
    
    // 4. Enviar respuesta
    return res.status(200).json(result);
    

  } catch (error) {
    logger.error('Error al llamar al servicio externo de evaluate:', error.message);

    if (error.response) {
      return res.status(error.response.status).json({
        error: 'Error from evaluate service',
        details: error.response.data,
      });
    }

    return res.status(500).json({ error: 'Evaluate service unavailable' });
  }
};

module.exports = { evaluate };
