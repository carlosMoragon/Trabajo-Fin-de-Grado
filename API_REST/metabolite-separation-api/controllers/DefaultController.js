const Controller = require('./Controller');
const service = require('../services/DefaultService');
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

const feedbackPOST = async (request, response) => {
  await Controller.handleRequest(request, response, service.feedbackPOST);
};

const feedbackGET = async (req, res) => {
  try {
    const result = await service.feedbackGET(req);
    res.status(200).json(result);
  } catch (error) {
    console.error('Controller error:', error);
    res.status(500).json({
      message: 'Internal server error',
    });
  }
};


module.exports = {
  evaluatePOST,
  experimentsPOST,
  familiesGET,
  predictPOST,
  recommendFamilyPOST,
  feedbackPOST,
  feedbackGET
};
