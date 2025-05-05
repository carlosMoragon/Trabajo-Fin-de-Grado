
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
    const cachedLog = await Log.findOne({ request: req.body }).sort({ 'respond.Score': -1 }).exec();

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

module.exports = { predict };
