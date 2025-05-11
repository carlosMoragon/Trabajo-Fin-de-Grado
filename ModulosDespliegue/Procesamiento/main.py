import json
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelos de entrada para las solicitudes
class ConfigInput(BaseModel):
    configuration: dict
    family: str

class PredictInput(BaseModel):
    family: str

class FamilyRecommendInput(BaseModel):
    configuration: dict

# --- Endpoints ---

@app.post("/evaluate")
def evaluate(config: ConfigInput):
    try:
        config_json = {
            "configuration": config.configuration,
            "family": config.family
        }
        output = subprocess.check_output(
            ['python', 'evaluate.py', json.dumps(config_json)],
            stderr=subprocess.STDOUT
        )
        return json.loads(output.decode('utf-8', errors='replace'))  # Reemplaza caracteres no decodificables
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8', errors='replace')  # Decodifica con 'replace' para evitar error
        raise HTTPException(status_code=500, detail=f"Error en el script evaluate.py: {error_output}")

@app.post("/predict")
def predict(data: PredictInput):
    try:
        output = subprocess.check_output(
            ['python', 'predict.py', data.family],
            stderr=subprocess.STDOUT
        )
        decoded = output.decode('utf-8', errors='replace')
        return json.loads(decoded)
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8', errors='replace')  # Decodifica con 'replace' para evitar error
        raise HTTPException(status_code=500, detail=f"Error en el script predict.py: {error_output}")

@app.post("/recommendFamily")
def recommend(configuration: FamilyRecommendInput):
    try:
        config_dict = configuration.dict()
        json_config = json.dumps(config_dict)
        print(json_config)
        output = subprocess.check_output(
            ['python', 'recommendFamily.py', json_config],
            stderr=subprocess.STDOUT
        )
        return json.loads(output)#.decode('utf-8', errors='replace'))  # Reemplaza caracteres no decodificables
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8', errors='replace')  # Decodifica con 'replace' para evitar error
        raise HTTPException(status_code=500, detail=f"Error en el script recommendFamily.py: {error_output}")
