const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');

router.post('/', (req, res) => {
  const config = req.body;

  if (!config || typeof config !== 'object') {
    return res.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  // Convertimos la configuración a un string JSON para pasarlo como argumento al script
  const jsonString = JSON.stringify(config);

  const pythonProcess = spawn('python', ['../../src/modelos/predict_family_lgbm.py', jsonString]);

  let resultData = '';
  let responseSent = false;

  pythonProcess.stdout.on('data', (data) => {
    resultData += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error('Python error:', data.toString());
    if (!responseSent) {
      res.status(500).json({ error: 'Python script error', details: data.toString() });
      responseSent = true;
    }
  });

  pythonProcess.on('close', (code) => {
    if (!responseSent) {
      if (code !== 0) {
        res.status(500).json({ error: 'Python script exited with an error code: ' + code });
        responseSent = true;
      } else {
        try {
          const result = JSON.parse(resultData);
          res.status(200).json(result);
        } catch (err) {
          console.error('Error parsing JSON from Python output:', err);
          res.status(500).json({ error: 'Invalid JSON output from Python script.' });
        }
      }
    }
  });
});

module.exports = router;