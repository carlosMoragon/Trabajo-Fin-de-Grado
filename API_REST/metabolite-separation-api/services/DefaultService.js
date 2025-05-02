/* eslint-disable no-unused-vars */
const Service = require('./Service');
const Experiments = require('../models/Experiments');
const Family = require('../models/Family');
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
      // Realizar la consulta en la base de datos para obtener solo las familias con API_version = 1
      const families = await Family.find({ API_version: '1' });

      // Devolver las familias en formato JSON
      resolve({
        success: true,
        data: families,
      });
    } catch (e) {
      // Si hay un error, rechazamos la promesa
      reject({
        success: false,
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

module.exports = {
  evaluatePOST,
  experimentsPOST,
  familiesGET,
  predictPOST,
  recommendFamilyPOST,
};
