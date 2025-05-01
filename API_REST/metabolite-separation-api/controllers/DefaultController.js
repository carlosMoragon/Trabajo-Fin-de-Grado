/*
const { spawn } = require('child_process');
const Controller = require('./Controller');


const recommendFamilyPOST = async (request, response) => {
  const config = request.body.config; // Suponemos que la configuración está en `req.body.config`

  // Validamos que la configuración esté presente y sea un objeto
  if (!config || typeof config !== 'object') {
    return response.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  // Convertimos el objeto a una cadena JSON para pasarlo al script de Python
  const jsonString = JSON.stringify(config);

  // Aquí invocamos el script de Python
  const pythonProcess = spawn('python', ['../../src/modelos/predict_family_lgbm.py', jsonString]);

  let resultData = '';
  let responseSent = false;

  // Recibimos los datos de salida del script Python
  pythonProcess.stdout.on('data', (data) => {
    resultData += data.toString();
  });

  // Capturamos cualquier error que ocurra en el script Python
  pythonProcess.stderr.on('data', (data) => {
    console.error('Python error:', data.toString());
    if (!responseSent) {
      response.status(500).json({ error: 'Python script error', details: data.toString() });
      responseSent = true;
    }
  });

  // Al finalizar el proceso de Python, procesamos los resultados
  pythonProcess.on('close', (code) => {
    if (!responseSent) {
      if (code !== 0) {
        response.status(500).json({ error: 'Python script exited with an error code: ' + code });
        responseSent = true;
      } else {
        try {
          // Intentamos parsear la salida del script como JSON
          const result = JSON.parse(resultData);
          response.status(200).json(result);
        } catch (err) {
          console.error('Error parsing JSON from Python output:', err);
          response.status(500).json({ error: 'Invalid JSON output from Python script.' });
        }
      }
    }
  });
};

// Controlador para el endpoint POST /evaluate
const evaluatePOST = async (request, response) => {
  await Controller.handleRequest(request, response, service.evaluatePOST);
};

// Controlador para el endpoint POST /experiments
const experimentsPOST = async (request, response) => {
  await Controller.handleRequest(request, response, service.experimentsPOST);
};

// Controlador para el endpoint GET /families
const familiesGET = async (request, response) => {
  await Controller.handleRequest(request, response, service.familiesGET);
};

const predictPOST = async (request, response) => {
  const { family } = request.body;

  // Validamos que el campo "family" esté presente
  if (!family) {
    return response.status(400).json({ error: 'Missing "family" field.' });
  }

  // Llamamos al script de Python pasando el "family" como argumento
  const pythonProcess = spawn('python', ['../../src/modelos/script_Bayess.py', family]);

  let resultData = '';
  let responseSent = false;

  // Recibimos los datos de salida del script Python
  pythonProcess.stdout.on('data', (data) => {
    resultData += data.toString(); // Almacenamos la salida del script
  });

  // Capturamos cualquier error que ocurra en el script Python
  pythonProcess.stderr.on('data', (data) => {
    console.error('Python error:', data.toString());
    if (!responseSent) {
      response.status(500).json({ error: 'Python script error', details: data.toString() });
      responseSent = true;
    }
  });

  // Al finalizar el proceso de Python, procesamos los resultados
  pythonProcess.on('close', (code) => {
    if (!responseSent) {
      if (code !== 0) {
        response.status(500).json({ error: 'Python script exited with an error code: ' + code });
        responseSent = true;
      } else {
        try {
          // Intentamos parsear la salida del script como JSON
          const result = JSON.parse(resultData);
          response.status(200).json(result); // Respondemos con el resultado final
        } catch (err) {
          console.error('Error parsing JSON from Python output:', err);
          response.status(500).json({ error: 'Invalid JSON output from Python script.' });
        }
      }
    }
  });
};

module.exports = {
  evaluatePOST,
  experimentsPOST,
  familiesGET,
  predictPOST,
  recommendFamilyPOST,
};
*/
/**
 * The DefaultController file is a very simple one, which does not need to be changed manually,
 * unless there's a case where business logic routes the request to an entity which is not
 * the service.
 * The heavy lifting of the Controller item is done in Request.js - that is where request
 * parameters are extracted and sent to the service, and where response is handled.
 */
/*
const Controller = require('./Controller');
const service = require('../services/DefaultService');
const evaluatePOST = async (request, response) => {
  await Controller.handleRequest(request, response, service.evaluatePOST);
};

const experimentsPOST = async (request, response) => {
  await Controller.handleRequest(request, response, service.experimentsPOST);
};

const familiesGET = async (request, response) => {
  await Controller.handleRequest(request, response, service.familiesGET);
};

const predictPOST = async (request, response) => {
  await Controller.handleRequest(request, response, service.predictPOST);
};

const recommendFamilyPOST = async (request, response) => {
  await Controller.handleRequest(request, response, service.recommendFamilyPOST);
};


module.exports = {
  evaluatePOST,
  experimentsPOST,
  familiesGET,
  predictPOST,
  recommendFamilyPOST,
}





*/

const Controller = require('./Controller');
const PredictService = require('../services/PredictService');
const RecommendFamilyService = require('../services/RecommendFamilyService');
const EvaluateService = require('../services/evaluateService');

const predictPOST = async (request, response) => {
  await PredictService.predict(request, response);
};

const recommendFamilyPOST = async (request, response) => {
  await RecommendFamilyService.recommendFamily(request, response);
};

const evaluatePOST = async (request, response) => {
  await EvaluateService.evaluate(request, response);//, service.evaluatePOST);
};

const experimentsPOST = async (request, response) => {
  await Controller.handleRequest(request, response, service.experimentsPOST);
};

const familiesGET = async (request, response) => {
  await Controller.handleRequest(request, response, service.familiesGET);
};

module.exports = {
  evaluatePOST,
  experimentsPOST,
  familiesGET,
  predictPOST,
  recommendFamilyPOST,
};
