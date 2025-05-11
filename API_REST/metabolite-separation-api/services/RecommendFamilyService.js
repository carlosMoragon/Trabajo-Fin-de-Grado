const config = require('../config');
const axios = require('axios');
//const RecommendFamily = require('../models/RecommendFamily');
const logger = require('../logger');

const recommendFamily = async (req, res) => {
  const { configuration } = req.body;
  const db_host = config.DATABASE_API_HOST;
  const db_port = config.DATABASE_API_PORT;
  const host = config.PREDICTOR_HOST;
  const port = config.PREDICTOR_PORT;

  if (!configuration || typeof configuration !== 'object') {
    return res.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  try {
    // 1. Revisar caché
    //const cachedResult = await RecommendFamily.findOne({ request: req.body }).sort({ 'respond.Score': -1 }).exec();
    
    const cachedResult = await axios.post(`http://${db_host}:${db_port}/recommendFamily/cache`, req.body);


    if (cachedResult.data.cached == true) {
      //cachedResult.cacheHits += 1;
      //await cachedResult.save();
      res.locals.responseAlreadySent = true;
      res.locals.calculatedResponse = cachedResult.data;
      res.status(200).json(cachedResult.data.result.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en recommendFamily:', err);
  }

  try {

    const response = await axios.post(`http://${host}:${port}/recommendFamily`, { configuration });
    const result = response.data;

    // 3. Guardar en caché
    setImmediate(async () => {
      try {
        await axios.post(`http://${db_host}:${db_port}/recommendFamily/save`, {
          API_version: 1,
          request: req.body,
          respond: result,
        });
      } catch (saveErr) {
        logger.error('Error guardando en la caché (recommendFamily):', saveErr);
      }
      /*
      try {
        await RecommendFamily.create({
          API_version: 1,
          request: req.body,
          respond: result,
        });
      } catch (saveErr) {
        logger.error('Error guardando en la caché de recommendFamily:', saveErr);
      }*/
    });

    // 4. Enviar la respuesta
    if (!res.locals.responseAlreadySent) {
      return res.status(200).json(result);
    }
  } catch (error) {
    logger.error('Error al llamar al servicio externo de recommendFamily:', error.message);

    if (error.response) {
      return res.status(error.response.status).json({
        error: 'Error from recommendFamily service',
        details: error.response.data,
      });
    }

    return res.status(500).json({ error: 'recommendFamily service unavailable' });
  }
};

module.exports = { recommendFamily };
