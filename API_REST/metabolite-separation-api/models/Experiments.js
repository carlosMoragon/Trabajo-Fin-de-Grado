const mongoose = require('mongoose');

const ExperimentSchema = new mongoose.Schema({
  name_metabolito: String,
  formula: String,
  rt: Number,
  smiles_std: String,
  inchi_std: String,
  inchikey_std: String,
  classyfire: {
    kingdom: String,
    superclass: String,
    class: String,
    subclass: String,
    level5: String,
    level6: String,
  },
  comment: String,
  alternative_parents: String,
  column: {
    name: String,
    usp_code: String,
    length: Number,
    particle_size: Number,
    temperature: Number,
    flowrate: Number,
    t0: Number,
  },
  gradiente: {
    eluyente1: String,
    eluyente1_gradiente: [Number],
    eluyente2: String,
    eluyente2_gradiente: [Number],
    t_gradiente: [Number],
    ph1: Number,
    ph2: Number
  }
});

module.exports = mongoose.model('experiments', ExperimentSchema);
