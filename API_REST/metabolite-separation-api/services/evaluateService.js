const { spawn } = require('child_process');

const evaluate = async (request, response) => {
  const body = request.body;

  if (!body || typeof body.configuration !== 'object') {
    return response.status(400).json({ error: 'Missing or invalid configuration object.' });
  }

  const jsonString = JSON.stringify(body);
  const pythonProcess = spawn('python', ['scripts/modelos/evaluate.py', jsonString]);

  let resultData = '';
  let responseSent = false;

  pythonProcess.stdout.on('data', (data) => {
    resultData += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error('Python error:', data.toString());
    if (!responseSent) {
      response.status(500).json({ error: 'Python script error', details: data.toString() });
      responseSent = true;
    }
  });

  pythonProcess.on('close', (code) => {
    if (!responseSent) {
      if (code !== 0) {
        response.status(500).json({ error: `Python script exited with code ${code}` });
      } else {
        try {
          const result = JSON.parse(resultData);
          response.status(200).json(result);
        } catch (err) {
          console.error('Error parsing Python output:', err);
          response.status(500).json({ error: 'Invalid JSON output from Python script.' });
        }
      }
      responseSent = true;
    }
  });
};

module.exports = { evaluate };
