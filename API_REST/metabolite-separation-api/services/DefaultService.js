/* eslint-disable no-unused-vars */
const Service = require('./Service');

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
* */
const experimentsPOST = ({ experimentRequest }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        experimentRequest,
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
* Retrieves a list of metabolite families.
* Returns a list of available metabolite families for the system.
*
* returns List
* */
const familiesGET = () => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
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
