/*
const { spawn } = require('child_process');
const Evaluate = require('../models/Evaluate'); 
const logger = require('../logger');

const evaluate = async (request, response) => {
  const body = request.body;

  if (!body || typeof body.configuration !== 'object') {
    return response.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  // 1. Revisar caché (Buscar en la base de datos)
  try {
    //const cachedResult = await Evaluate.findOne({ request: request.body });
    const cachedResult = await Log.findOne({ request: req.body }).sort({ 'respond.body.Score': -1 }).exec();

    if (cachedResult) {
      // Si se encuentra un resultado en caché, actualizar el contador de hits
      cachedResult.cacheHits += 1;
      await cachedResult.save();

      // Enviar la respuesta desde la caché
      return response.status(200).json(cachedResult.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en evaluate:', err);
  }

  console.log("SE SIGUE PROCESANDO");

  // 2. Ejecutar el proceso de Python (en segundo plano) se ejecute o no haya caché.
  const jsonString = JSON.stringify(body);
  const pythonProcess = spawn('python', ['scripts/modelos/evaluate.py', jsonString]);

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
            setImmediate(async () => {
              try {
                await Evaluate.create({  // Usamos el modelo 'Evaluate'
                  API_version: 1,
                  request: request.body,
                  respond: result,
                });
              } catch (saveErr) {
                logger.error('Error guardando en la caché de evaluate:', saveErr);
              }
            });
          } catch (saveErr) {
            logger.error('Error guardando en la caché de evaluate:', saveErr);
          }

          // 4. Enviar la respuesta final
          response.status(200).json(result);
        } catch (err) {
          console.error('Error parsing Python output:', err);
          response.status(500).json({ error: 'Invalid JSON output from Python script.' });
        }
      }
      responseSent = true;
    }
  });
};

module.exports = { evaluate };
*/
//require('dotenv').config();
const config = require('../config');
const axios = require('axios');
const Evaluate = require('../models/Evaluate');
const logger = require('../logger');

const evaluate = async (req, res) => {
  const body = req.body;

  if (!body || typeof body.configuration !== 'object') {
    return res.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  try {
    // 1. Revisar caché
    const cachedResult = await Evaluate.findOne({ request: req.body }).sort({ 'respond.Score': -1 }).exec();

    if (cachedResult) {
      cachedResult.cacheHits += 1;
      await cachedResult.save();
      return res.status(200).json(cachedResult.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en evaluate:', err);
  }

  try {
    // 2. Llamar al servicio externo /evaluate
    const host = config.PREDICTOR_HOST;
    const port = config.PREDICTOR_PORT;

    const response = await axios.post(`http://${host}:${port}/evaluate`, body);
    const result = response.data;

    // 3. Guardar resultado en caché
    setImmediate(async () => {
      try {
        await Evaluate.create({
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
