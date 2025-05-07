/*
const { spawn } = require('child_process');
const RecommendFamily = require('../models/RecommendFamily'); // Modelo de caché
const logger = require('../logger');

const recommendFamily = async (request, response) => {
  const { config } = request.body;

  if (!config || typeof config !== 'object') {
    return response.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  // 1. Revisar caché (Buscar en la base de datos)
  try {
    const cachedResult = await Log.findOne({ request: req.body }).sort({ 'respond.Score': -1 }).exec();

    if (cachedResult) {
      // Si se encuentra un resultado en caché, actualizar el contador de hits
      cachedResult.cacheHits += 1;
      await cachedResult.save();

      // Indicar que ya se ha enviado una respuesta
      response.locals.responseAlreadySent = true;
      response.locals.calculatedResponse = cachedResult.respond;

      // Enviar la respuesta desde la caché
      response.status(200).json(cachedResult.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en recommendFamily:', err);
  }


  // 2. Ejecutar el proceso de Python (en segundo plano) se ejecute o no haya caché.
  const jsonString = JSON.stringify(config); // Convertir config a JSON
  const pythonProcess = spawn('python', ['scripts/modelos/recommendFamily.py', jsonString]);

  let resultData = '';
  let responseSent = false;

  pythonProcess.stdout.on('data', (data) => {
    resultData += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error('Python error:', data.toString());
    if (!responseSent) {
      response.status(500).json({ error: 'Python script error', details: data.toString() });
      responseSent = true;
    }
  });

  pythonProcess.on('close', async (code) => {
    if (!responseSent) {
      if (code !== 0) {
        response.status(500).json({ error: `Python script exited with code ${code}` });
      } else {
        try {
          const result = JSON.parse(resultData);

          // 3. Guardar el resultado del script en la base de datos (caché)
          try {
            // Usamos setImmediate para no bloquear el flujo de respuesta
            setImmediate(async () => {
              try {
                await RecommendFamily.create({
                  API_version: 1,
                  request: request.body,
                  respond: result,
                });
              } catch (saveErr) {
                logger.error('Error guardando en la caché de recommendFamily:', saveErr);
              }
            });
          } catch (saveErr) {
            logger.error('Error guardando en la caché de recommendFamily:', saveErr);
          }

          // 4. Enviar la respuesta final
          if (!response.locals.responseAlreadySent) {
            response.status(200).json(result);
          }
        } catch (err) {
          console.error('Error parsing Python output:', err);
          response.status(500).json({ error: 'Invalid JSON output from Python script.' });
        }
      }
      responseSent = true;
    }
  });
};

module.exports = { recommendFamily };
*/
require('dotenv').config();
const axios = require('axios');
const RecommendFamily = require('../models/RecommendFamily');
const logger = require('../logger');

const recommendFamily = async (req, res) => {
  const { config } = req.body;

  if (!config || typeof config !== 'object') {
    return res.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  try {
    // 1. Revisar caché
    const cachedResult = await RecommendFamily.findOne({ request: req.body }).sort({ 'respond.Score': -1 }).exec();

    if (cachedResult) {
      cachedResult.cacheHits += 1;
      await cachedResult.save();
      return res.status(200).json(cachedResult.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en recommendFamily:', err);
  }

  try {
    // 2. Llamar al microservicio externo
    const host = process.env.PREDICTOR_HOST;
    const port = process.env.PREDICTOR_PORT;

    const response = await axios.post(`http://${host}:${port}/recommendFamily`, { config });
    const result = response.data;

    // 3. Guardar en caché
    setImmediate(async () => {
      try {
        await RecommendFamily.create({
          API_version: 1,
          request: req.body,
          respond: result,
        });
      } catch (saveErr) {
        logger.error('Error guardando en la caché de recommendFamily:', saveErr);
      }
    });

    // 4. Enviar la respuesta
    return res.status(200).json(result);
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
