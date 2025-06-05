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

    
        return [FeedbackModel(**d) for d in cleaned]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feedbacks: {e}")