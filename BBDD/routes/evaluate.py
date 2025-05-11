from fastapi import APIRouter, HTTPException
from models import RequestResponseModel, EvaluateCacheModel
from db import evaluates
from pymongo import DESCENDING
from utils import with_clean_mongo_id

router = APIRouter()

# Ruta para consultar la caché
@router.post("/cache")
@with_clean_mongo_id(remove_id=True) 
async def evaluate_cache(data: EvaluateCacheModel):
    # Buscar en la caché
    #print(data.dict(exclude_unset=True))
    cached = await evaluates.find_one(
        {"request": data.dict(exclude_unset=True)}, sort=[("respond.Score", DESCENDING)]
    )

    if cached:
        cached['cacheHits'] = cached.get('cacheHits', 0) + 1
        await evaluates.replace_one({"_id": cached["_id"]}, cached)
        return {"cached": True, "result": cached}
    else:
        return {"cached": False, "result": None}

    raise HTTPException(status_code=404, detail="Cache not found")

# Ruta para guardar un resultado en la caché
@router.post("/save")
async def evaluate_save(data: RequestResponseModel):
    # Guardar en la base de datos
    try:
        await evaluates.insert_one(data.dict())
        return {"stored": True, "message": "Result successfully stored in cache."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving result: {e}")
