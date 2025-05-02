const mongoose = require('mongoose');

const FamilySchema = new mongoose.Schema({
    family: String,
    CHEMONTID: String,
    API_version: String,
  });
  
  // Definir el modelo de Mongoose basado en el esquema
  module.exports = mongoose.model('Family', FamilySchema);