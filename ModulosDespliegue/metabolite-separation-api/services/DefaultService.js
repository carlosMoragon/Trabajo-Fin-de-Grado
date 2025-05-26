/* eslint-disable no-unused-vars */
const Service = require('./Service');
const axios = require('axios');
const config = require('../config');
/**
* Evaluates the alpha score for a given configuration.
* Evaluates how good a configuration is for a metabolite family by calculating the alpha score.
*
* evaluateRequest EvaluateRequest  (optional)
* returns EvaluateResponse
* */
const evaluatePOST = ({ evaluateRequest }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        evaluateRequest,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
 * Adds an experiment to the database.
 * Adds new experiment data to the system.
 *
 * experimentRequest ExperimentRequest  (optional)
 * no response value expected for this operation
 */
const experimentsPOST = (request) => new Promise(
  async (resolve, reject) => {
    try {
      const experimentRequest = request.body;
      const db_host = config.DATABASE_API_HOST;
      const db_port = config.DATABASE_API_PORT;
      //console.log('Datos de experimentRequest:', experimentRequest);

      const response = await axios.post(`http://${db_host}:${db_port}/experiments`, experimentRequest, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      //console.log('Respuesta del backend:', response.data);
      //resolve(response.data);
      resolve(Service.successResponse({
        message: 'Data received',
        data: response.data
      }));
    } catch (e) {
      //console.error('Error forwarding experiment(s):', e.message);
      reject(Service.rejectResponse(
        'Failed to forward experiment(s)',
        500
      ));
    }
  },
);

/**
* Retrieves a list of metabolite families.
* Returns a list of available metabolite families for the system.
*
* returns List
* */
const familiesGET = () => new Promise(
  async (resolve, reject) => {
    const db_host = config.DATABASE_API_HOST;
    const db_port = config.DATABASE_API_PORT;
    try {
      const response = await axios.get(`http://${db_host}:${db_port}/families`);

      resolve({
        families: response.data
      });
    } catch (e) {
      console.error('Error al redirigir la solicitud de familias:', e.message);

      reject({
        message: e.message || 'Error al obtener las familias desde el backend',
        status: e.response?.status || 500,
      });
    }
  },
);


/**
* Predicts the best configuration to separate a metabolite family.
* Given a metabolite family, it returns the best configuration to separate them.
*
* familyRequest FamilyRequest  (optional)
* returns PredictResponse
* */
const predictPOST = ({ familyRequest }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        familyRequest,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* Recommends the most suitable metabolite family for a given configuration.
* Given a configuration, recommends the most appropriate metabolite family.
*
* configuration Configuration  (optional)
* no response value expected for this operation
* */
const recommendFamilyPOST = ({ configuration }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        configuration,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);


const feedbackPOST = (request) => new Promise(
  async (resolve, reject) => {
    try {
      const feedbackRequest = request.body;
      const db_host = config.DATABASE_API_HOST;
      const db_port = config.DATABASE_API_PORT;
      console.log('Redirigiendo feedbackPOST con datos:', feedbackRequest);

      const response = await axios.post(`http://${db_host}:${db_port}/feedbacks`, feedbackRequest);

      resolve(response.data);
      /*resolve(Service.successResponse({
        message: 'Feedback(s) saved successfully (via proxy)',
        data: response.data
      }));*/
    } catch (e) {
      console.error('Error al redirigir feedbackPOST:', e.message);
      reject(Service.rejectResponse(
        'Failed to save feedback(s) via proxy',
        e.response?.status || 400
      ));
    }
  },
);

const feedbackGET = (request) => new Promise(
  async (resolve, reject) => {
    try {
      const queryParams = request.query;
      const db_host = config.DATABASE_API_HOST;
      const db_port = config.DATABASE_API_PORT;
      console.log('Redirigiendo feedbackGET con query:', queryParams);

      const response = await axios.get(`http://${db_host}:${db_port}/feedbacks`, {
        params: queryParams
      });
      resolve(response.data);
      /*resolve(Service.successResponse({
        message: 'Feedbacks retrieved successfully (via proxy)',
        data: response.data
      }));*/
    } catch (e) {
      console.error('Error al redirigir feedbackGET:', e.message);
      reject(Service.rejectResponse(
        'Failed to retrieve feedbacks',
        e.response?.status || 500
      ));
    }
  }
);





module.exports = {
  evaluatePOST,
  experimentsPOST,
  familiesGET,
  predictPOST,
  recommendFamilyPOST,
  feedbackPOST,
  feedbackGET
};
