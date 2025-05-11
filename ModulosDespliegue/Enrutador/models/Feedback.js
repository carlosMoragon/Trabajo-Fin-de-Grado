const mongoose = require('mongoose');

const FeedbackSchema = new mongoose.Schema({
  family: { type: String, required: true },
  score: { type: Number, required: true },
  feedback: { type: Number, required: true },
  configuration: {
    eluent1: String,
    eluent2: String,
    ph1: Number,
    ph2: Number,
    column: {
      uspCode: String,
      length: Number,
      name: String,
      particleSize: Number,
      temperature: Number,
      flowrate: Number,
      t0: Number
    },
    gradient: {
      x0: Number, x1: Number, x2: Number, x3: Number, x4: Number,
      x5: Number, x6: Number, x7: Number, x8: Number, x9: Number,
      x10: Number, duration: Number
    }
  }
});

module.exports = mongoose.model('Feedback', FeedbackSchema, 'feedbacks');
