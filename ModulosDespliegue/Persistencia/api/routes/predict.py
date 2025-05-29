'''from fastapi import APIRouter, HTTPException
from models import RequestResponseModel, PredictCacheModel
from db import predicts
from pymongo import DESCENDING
from utils import with_clean_mongo_id

router = APIRouter()

# Ruta para consultar la caché
@router.post("/cache")
@with_clean_mongo_id(remove_id=True) 
async def predict_cache(data: PredictCacheModel):
    cached = await predicts.find_one(
        {"request.family": data.family},
        sort=[("respond.Score", DESCENDING)]
    )

    if cached:
        cached['cacheHits'] = cached.get('cacheHits', 0) + 1
        await predicts.replace_one({"_id": cached["_id"]}, cached)
        return {"cached": True, "result": cached}
    else:
        return {"cached": False, "result": None}
    raise HTTPException(status_code=404, detail="Cache not found for provided family.")

# Ruta para guardar un resultado en la caché
@router.post("/save")
async def predict_save(data: RequestResponseModel):
    # Guardar en la base de datos
    try:
        await predicts.insert_one(data.dict())
        return {"stored": True, "message": "Result successfully stored in cache."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving result: {e}")
'''
from fastapi import APIRouter, HTTPException
from models import RequestResponseModel, PredictCacheModel
from db import predicts
from pymongo import DESCENDING
from utils import with_clean_mongo_id

router = APIRouter()

# Ruta para consultar la caché
@router.post("/cache")
@with_clean_mongo_id(remove_id=True)
async def predict_cache(data: PredictCacheModel):
    cached = await predicts.find_one(
        {"request.class": data.class_},
        sort=[("respond.score", DESCENDING)]
    )

    if cached:
        cached['cacheHits'] = cached.get('cacheHits', 0) + 1
        await predicts.replace_one({"_id": cached["_id"]}, cached)
        return {"cached": True, "result": cached}
    else:
        return {"cached": False, "result": None}

# Ruta para guardar un resultado en la caché
@router.post("/save")
async def predict_save(data: RequestResponseModel):
    try:
        await predicts.insert_one(data.dict())
        return {"stored": True, "message": "Result successfully stored in cache."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving result: {e}")
