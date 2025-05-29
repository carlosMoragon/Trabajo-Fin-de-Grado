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
from fastapi import APIRouter, HTTPException 
from models import FeedbackModel
from db import feedbacks
from utils import with_clean_mongo_id

router = APIRouter()

# Ruta para agregar un feedback
@router.post("/", response_model=dict)
async def add_feedback(feedback_request: FeedbackModel):
    try:
        await feedbacks.insert_one(feedback_request.dict())
        return {"message": "Feedback saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving feedback: {e}")

# Ruta para obtener feedbacks (opcionalmente filtrado por familia)
#async def get_feedback(familyname: str = None):
@router.get("/", response_model=list[FeedbackModel])
@with_clean_mongo_id(remove_id=True)
async def get_feedback(classname: str = None):
    try:
        if classname:
            feedbacks_list = await feedbacks.find({"class": classname}).to_list(length=None)
        else:
            feedbacks_list = await feedbacks.find().to_list(length=None)

        # Asegurarse que cada elemento cumple el modelo
        return [FeedbackModel(**item) for item in feedbacks_list]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedbacks: {e}")