/* eslint-disable no-unused-vars */
const Service = require('./Service');
const Experiments = require('../models/Experiments');
const Family = require('../models/Family');
const Feedbacks = require('../models/Feedback');
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
);
/**
* Retrieves a list of metabolite families.
* Returns a list of available metabolite families for the system.
*
* returns List
* */
const familiesGET = () => new Promise(
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
    try {
      // Obtener el parámetro "nombrefamilia" de la consulta (query)
      const familyName = request.query.nombrefamilia;

      let feedbacks;

      // Si familyName existe, filtrar los feedbacks por esa familia
      if (familyName) {
        feedbacks = await Feedbacks.find({ family: familyName });
        console.log(`Feedbacks encontrados para la familia: ${familyName}`);
      } else {
        // Si no se pasa "nombrefamilia", traer todos los feedbacks
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





module.exports = {
  evaluatePOST,
  experimentsPOST,
  familiesGET,
  predictPOST,
  recommendFamilyPOST,
  feedbackPOST,
  feedbackGET
};
