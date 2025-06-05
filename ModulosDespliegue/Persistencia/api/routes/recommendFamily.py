from fastapi import APIRouter, HTTPException
from models import RequestResponseModel, RecommendFamilyCacheModel, Config
from db import recommendfamilies
from pymongo import DESCENDING
from utils import with_clean_mongo_id

router = APIRouter()

# Ruta para consultar la caché
@router.post("/cache")
@with_clean_mongo_id(remove_id=True)
async def recommend_family_cache(data: RecommendFamilyCacheModel):
    cached = await recommendfamilies.find_one(
        {"request": data.dict(exclude_unset=True)},
        sort=[("respond.score", DESCENDING)]
    )

    if cached:
        cached['cacheHits'] = cached.get('cacheHits', 0) + 1
        await recommendfamilies.replace_one({"_id": cached["_id"]}, cached)
        return {"cached": True, "result": cached}
    else:
        return {"cached": False, "result": None}

# Ruta para guardar un resultado en la caché
@router.post("/save")
async def recommend_family_save(data: RequestResponseModel):
    try:
        await recommendfamilies.insert_one(data.dict())
        return {"stored": True, "message": "Result successfully stored in cache."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving result: {e}")
