'''
from fastapi import APIRouter, HTTPException
from models import ExperimentModel
from db import experiments
from typing import List

router = APIRouter()

@router.post("/")
async def add_experiments(experiment_requests: List[ExperimentModel]):
    try:
        docs = [exp.dict() for exp in experiment_requests]
        await experiments.insert_many(docs)
        return {"message": "Experiments saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving experiments: {e}")
'''
from fastapi import APIRouter, HTTPException
from models import ExperimentModel
from db import experiments
from typing import List

router = APIRouter()

@router.post("/")
async def add_experiments(experiment_requests: List[ExperimentModel]):
    try:
        # Guardamos respetando los alias definidos en los modelos
        docs = [exp.dict(by_alias=True, exclude_unset=True) for exp in experiment_requests]
        await experiments.insert_many(docs)
        return {"message": "Experiments saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving experiments: {e}")
