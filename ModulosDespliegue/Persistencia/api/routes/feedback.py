'''from fastapi import APIRouter, HTTPException
from models import FeedbackModel
from db import feedbacks
from utils import with_clean_mongo_id

router = APIRouter()

# Ruta para agregar un feedback
@router.post("/")
async def add_feedback(feedback_request: FeedbackModel):
    try:
        await feedbacks.insert_one(feedback_request.dict())
        return {"message": "Feedback saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving feedback: {e}")

@router.get("/")
@with_clean_mongo_id(remove_id=True) 
async def get_feedback(familyname: str = None):
    try:
        if familyname:
            feedbacks_list = await feedbacks.find({"family": familyname}).to_list(length=None)
        else:
            feedbacks_list = await feedbacks.find().to_list(length=None)

        return {"message": "Feedback(s) retrieved successfully", "data": feedbacks_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedbacks: {e}")
'''

from fastapi import APIRouter, HTTPException, Query
from models import FeedbackModel
from db import feedbacks
from utils import with_clean_mongo_id
from typing import List, Optional

router = APIRouter()

# Ruta para agregar un feedback
@router.post("/", response_model=dict)
async def add_feedback(feedback_request: FeedbackModel):
    try:
        await feedbacks.insert_one(feedback_request.dict())
        return {"message": "Feedback saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving feedback: {e}")
@router.get("/", response_model=list[FeedbackModel])
@with_clean_mongo_id(remove_id=True)
async def get_feedback(classname: Optional[str] = Query(None, alias="classname")):
    """
    Si pasas ?classname=Foo, filtra por Foo en el campo 'class' o en 'class_'.
    Si no pasas nada, devuelve todos.
    Luego renombra siempre 'class_' → 'class' antes de instanciar.
    """
    # construye filtro opcional basándote en tu código original
    if classname:
        filt = {"$or": [{"class": classname}, {"class_": classname}]}
    else:
        filt = {}

    try:
        docs = await feedbacks.find(filt, {"_id": 0}).to_list(length=None)

        cleaned = []
        for d in docs:
            # si viene "class_", lo movemos a "class"
            if "class_" in d:
                d["class"] = d.pop("class_")
            cleaned.append(d)

        # instanciamos FeedbackModel para validar y usar el alias "class"
        return [FeedbackModel(**d) for d in cleaned]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedbacks: {e}")
'''async def get_feedback(classname: Optional[str] = Query(None, alias="classname")):
    docs = await feedbacks.find(
        {"class": classname} if classname else {},
        {"_id": 0}
    ).to_list(length=None)

    cleaned = []
    for d in docs:
        # si el documento trae "class_", lo pasamos a "class"
        if "class_" in d:
            d["class"] = d.pop("class_")
        cleaned.append(d)

    # ahora cada dict tiene "class" y Pydantic casará perfectamente
    return [FeedbackModel(**d) for d in cleaned]'''
'''async def get_feedback(classname: str = None):
    try:
        if classname:
            feedbacks_list = await feedbacks.find({"class": classname}).to_list(length=None)
        else:
            feedbacks_list = await feedbacks.find().to_list(length=None)

        # Asegurarse que cada elemento cumple el modelo
        return [FeedbackModel(**item) for item in feedbacks_list]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedbacks: {e}")'''