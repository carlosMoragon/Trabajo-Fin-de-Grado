/* eslint-disable no-unused-vars */
const Service = require('./Service');
const Experiments = require('../models/Experiments');
const Family = require('../models/Family');
const Feedbacks = require('../models/Feedback');
const axios = require('axios');
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
      //console.log('Datos de experimentRequest:', experimentRequest);

      const response = await axios.post('http://localhost:8010/experiments', experimentRequest, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      //console.log('Respuesta del backend:', response.data);

      resolve(Service.successResponse({
        message: 'Experiment(s) forwarded successfully',
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
/*const experimentsPOST = (request) => new Promise(
  async (resolve, reject) => {
    try {
      const experimentRequest = request.body;
      console.log('Datos de experimentRequest:', experimentRequest);

      if (Array.isArray(experimentRequest)) {
        await Experiments.insertMany(experimentRequest);
        console.log('Experimentos insertados correctamente');
      } else {
        const newExperiment = new Experiments(experimentRequest);
        console.log('Nuevo experimento:', newExperiment);
        await newExperiment.save();
      }

      resolve(Service.successResponse({
        message: 'Experiment(s) saved successfully'
      }));
    } catch (e) {
      console.error('Error saving experiment(s):', e);
      reject(Service.rejectResponse(
        'Failed to save experiment(s)',
        400
      ));
    }
  },
);*/
/**
* Retrieves a list of metabolite families.
* Returns a list of available metabolite families for the system.
*
* returns List
* */
const familiesGET = () => new Promise(
  async (resolve, reject) => {
    try {
      const response = await axios.get('http://localhost:8010/families');

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

/*const familiesGET = () => new Promise(
  async (resolve, reject) => {
    try {
      // Solo seleccionamos los campos "family" y "CHEMONTID"
      const families = await Family.find({ API_version: '1' }).select('family CHEMONTID -_id');

      resolve({
        families
      });
    } catch (e) {
      reject({
        message: e.message || 'Error al obtener las familias',
        status: e.status || 500,
      });
    }
  },
);*/

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
/*
const feedbackPOST = (request) => new Promise(
  async (resolve, reject) => {
    try {
      const feedbackRequest = request.body;
      console.log('Datos de feedbackRequest:', feedbackRequest);

      if (Array.isArray(feedbackRequest)) {
        await Feedbacks.insertMany(feedbackRequest);
        console.log('Feedbacks insertados correctamente');
      } else {
        const newFeedback = new Feedbacks(feedbackRequest);
        console.log('Nuevo feedback:', newFeedback);
        await newFeedback.save();
      }

      resolve(Service.successResponse({
        message: 'Feedback(s) saved successfully'
      }));
    } catch (e) {
      console.error('Error saving feedback(s):', e);
      reject(Service.rejectResponse(
        'Failed to save feedback(s)',
        400
      ));
    }
  },
);

const feedbackGET = (request) => new Promise( 
  async (resolve, reject) => {
    console.log('Request.query:', request.query);
    try {
      
      const familyName = request.query.familyname;
      
      let feedbacks;

      if (familyName) {
        feedbacks = await Feedbacks.find({ family: familyName });
        console.log(`Feedbacks encontrados para la familia: ${familyName}`);
      } else {
        
        feedbacks = await Feedbacks.find();
        console.log('Todos los feedbacks:', feedbacks);
      }

      // Responder con los feedbacks encontrados
      resolve(Service.successResponse({
        message: 'Feedbacks retrieved successfully',
        data: feedbacks
      }));
    } catch (e) {
      console.error('Error retrieving feedbacks:', e);
      reject(Service.rejectResponse(
        'Failed to retrieve feedbacks',
        500
      ));
    }
  }
);
*/

const feedbackPOST = (request) => new Promise(
  async (resolve, reject) => {
    try {
      const feedbackRequest = request.body;
      console.log('Redirigiendo feedbackPOST con datos:', feedbackRequest);

      const response = await axios.post('http://localhost:8010/feedbacks', feedbackRequest);

      resolve(Service.successResponse({
        message: 'Feedback(s) saved successfully (via proxy)',
        data: response.data
      }));
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
      console.log('Redirigiendo feedbackGET con query:', queryParams);

      const response = await axios.get('http://localhost:8010/feedbacks', {
        params: queryParams
      });

      resolve(Service.successResponse({
        message: 'Feedbacks retrieved successfully (via proxy)',
        data: response.data
      }));
    } catch (e) {
      console.error('Error al redirigir feedbackGET:', e.message);
      reject(Service.rejectResponse(
        'Failed to retrieve feedbacks via proxy',
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
