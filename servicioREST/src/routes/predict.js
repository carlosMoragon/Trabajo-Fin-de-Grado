const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');

router.post('/', (req, res) => {
  const { family } = req.body;

  if (!family) {
    return res.status(400).json({ error: 'Missing "family" field.' });
  }

  // Llamar al script Python pasando la clase del metabolito como argumento
  const pythonProcess = spawn('python', ['../../src/modelos/script_Bayess.py', family]);

  // Variable para almacenar la respuesta del proceso Python
  let responseSent = false;
  let resultData = null;

  pythonProcess.stdout.on('data', (data) => {
    // No enviar respuesta durante los trials
    // Guardar los resultados del último trial
    resultData = data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error('Python error:', data.toString());
    if (!responseSent) {
      res.status(500).json({ error: 'Python script error' });
      responseSent = true;
    }
  });

  pythonProcess.on('close', (code) => {
    // Solo enviamos la respuesta una vez el script haya terminado
    if (!responseSent) {
      if (code !== 0) {
        res.status(500).json({ error: 'Python script finished with an error' });
        responseSent = true;
      } else {
        try {
          // Parsear el resultado final del último trial
          const result = JSON.parse(resultData);
          res.status(200).json(result); // Enviar el resultado final
          responseSent = true;
        } catch (error) {
          console.error('Error parsing Python result:', error);
          res.status(500).json({ error: 'Error processing prediction' });
          responseSent = true;
        }
      }
    }
  });
});

module.exports = router;