import json
import subprocess
from fastapi import FastAPI, HTTPException
from models import (
    EvaluateInput, PredictInput, FamilyRecommendInput,
    EvaluateOutput, PredictOutput, RecommendFamilyOutput
)

app = FastAPI()


@app.post("/evaluate", response_model=EvaluateOutput, tags=["Evaluation"])
def evaluate(config: EvaluateInput):
    try:
        config_json = {
            "configuration": config.configuration.dict(),
            "class": config.class_
        }
        output = subprocess.check_output(
            ['python', 'evaluate.py', json.dumps(config_json)],
            stderr=subprocess.STDOUT
        )
        return json.loads(output.decode('utf-8', errors='replace'))
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8', errors='replace')
        raise HTTPException(status_code=500, detail=f"Error en evaluate.py: {error_output}")


@app.post("/predict", response_model=PredictOutput, tags=["Prediction"])
def predict(data: PredictInput):
    try:
        output = subprocess.check_output(
            ['python', 'predict.py', data.class_],
            stderr=subprocess.STDOUT
        )
        return json.loads(output.decode('utf-8', errors='replace'))
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8', errors='replace')
        raise HTTPException(status_code=500, detail=f"Error en predict.py: {error_output}")


@app.post("/recommendFamily", response_model=RecommendFamilyOutput, tags=["Family Recommendation"])
def recommend(configuration: FamilyRecommendInput):
    try:
        config_json = {
            "configuration": configuration.configuration.dict()
        }
        output = subprocess.check_output(
            ['python', 'recommendFamily.py', json.dumps(config_json)],
            stderr=subprocess.STDOUT
        )
        return json.loads(output.decode('utf-8', errors='replace'))
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8', errors='replace')
        raise HTTPException(status_code=500, detail=f"Error en recommendFamily.py: {error_output}")
