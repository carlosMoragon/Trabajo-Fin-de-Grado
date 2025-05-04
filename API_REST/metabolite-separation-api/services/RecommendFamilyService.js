/*
const { spawn } = require('child_process');
const Log = require('../models/Predict');
const logger = require('../logger');

const predict = async (req, res) => {
  const { family } = req.body;

  if (!family) {
    return res.status(400).json({ error: 'Missing "family" field.' });
  }

  // 1. Revisar caché (Buscar en la base de datos)
  try {
    const cachedLog = await Log.findOne({ request: req.body });

    if (cachedLog) {
      // Si se encuentra un log en caché, actualizar el contador de hits
      cachedLog.cacheHits += 1;
      await cachedLog.save();

      // Indicar que ya se ha enviado una respuesta
      res.locals.responseAlreadySent = true;
      res.locals.calculatedResponse = cachedLog.respond;

      // Enviar la respuesta desde la caché
      res.status(200).json(cachedLog.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en predict:', err);
  }
  console.log("SE SIGUE PROCESANDO");
  // 2. Ejecutar el proceso de Python (en segundo plano) se encuentre o no la respuesta en caché.
  const pythonProcess = spawn('python', ['./scripts/modelos/predict.py', family]);

  let resultData = '';

  pythonProcess.stdout.on('data', (data) => {
    resultData += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    logger.error('Error del script Python:', data.toString());

    // Si el proceso Python falla, responder solo si no se ha respondido ya
    if (!res.locals.responseAlreadySent) {
      res.status(500).json({ error: 'Python script error', details: data.toString() });
    }
  });

  pythonProcess.on('close', async (code) => {
    if (code !== 0) {
      // Si el proceso de Python falla, responder solo si no se ha respondido ya
      if (!res.locals.responseAlreadySent) {
        res.status(500).json({ error: `Python script exited with code ${code}` });
      }
      return;
    }

    try {
      const result = JSON.parse(resultData);

      // 3. Guardar el resultado del script en la base de datos (caché)
      try {
        // Usamos setImmediate para evitar bloquear el flujo de respuesta
        setImmediate(async () => {
          try {
            await Log.create({
              API_version: 1,
              request: req.body,
              respond: result,
            });
          } catch (saveErr) {
            logger.error('Error guardando en la caché:', saveErr);
          }
        });
      } catch (saveErr) {
        logger.error('Error guardando en la caché:', saveErr);
      }

      // 4. Si no se respondió antes, enviar la respuesta final
      if (!res.locals.responseAlreadySent) {
        res.status(200).json(result);
      }

    } catch (parseErr) {
      logger.error('Error al parsear la salida del script Python:', parseErr);
      // Si el parseo de JSON falla, responder solo si no se ha respondido ya
      if (!res.locals.responseAlreadySent) {
        res.status(500).json({ error: 'Invalid JSON output from Python script.' });
      }
    }
  });
};

const { spawn } = require('child_process');

const recommendFamily = async (request, response) => {
  const config = request.body.config;

  if (!config || typeof config !== 'object') {
    return response.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  try {
    const cachedLog = await Log.findOne({ request: req.body });

    if (cachedLog) {
      // Si se encuentra un log en caché, actualizar el contador de hits
      cachedLog.cacheHits += 1;
      await cachedLog.save();

      // Indicar que ya se ha enviado una respuesta
      res.locals.responseAlreadySent = true;
      res.locals.calculatedResponse = cachedLog.respond;

      // Enviar la respuesta desde la caché
      res.status(200).json(cachedLog.respond);
    }
  } catch (err) {
    logger.error('Error al consultar la caché en predict:', err);
  }

  console.log("SE SIGUE PROCESANDO");
  const jsonString = JSON.stringify(config);
  //const pythonProcess = spawn('python', ['scripts/modelos/predict_family_lgbm.py', jsonString]);
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

  pythonProcess.on('close', (code) => {
    if (!responseSent) {
      if (code !== 0) {
        response.status(500).json({ error: `Python script exited with code ${code}` });
      } else {
        try {
          const result = JSON.parse(resultData);
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

module.exports = { recommendFamily };
*/
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
    const cachedResult = await RecommendFamily.findOne({ request: request.body });

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

  console.log("SE SIGUE PROCESANDO");

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
