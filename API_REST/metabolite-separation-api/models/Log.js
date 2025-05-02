// models/Log.js
const mongoose = require('mongoose');

const logSchema = new mongoose.Schema({
  API_version: {
    type: Number,
    default: 1,
  },
  request: {
    type: Object,
    required: true,
  },
  respond: {
    type: Object,
    required: true,
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

module.exports  = mongoose.model('Log', logSchema);