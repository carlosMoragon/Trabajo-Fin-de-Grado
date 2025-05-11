from fastapi import APIRouter, HTTPException
from db import families
from models import FamilyModel
from utils import with_clean_mongo_id  

router = APIRouter()

@router.get("/", response_model=list[FamilyModel])
@with_clean_mongo_id(remove_id=True) 
async def get_families():
    try:
        docs = await families.find().to_list(length=None)
        return docs 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las familias: {e}")
