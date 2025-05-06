const mongoose = require('mongoose');

const FamilySchema = new mongoose.Schema({
    family: String,
    CHEMONTID: String,
    API_version: String,
  });
  
  
module.exports = mongoose.model('Family', FamilySchema);