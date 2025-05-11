from fastapi import FastAPI
from routes import experiments, families, feedback, recommendFamily, evaluate, predict
#from config import settings
import logging
import uvicorn

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Rutas para las operaciones
app.include_router(experiments.router, prefix="/experiments", tags=["Experiments"])
app.include_router(families.router, prefix="/families", tags=["Families"])
app.include_router(feedback.router, prefix="/feedbacks", tags=["Feedbacks"])
app.include_router(recommendFamily.router, prefix="/recommendFamily", tags=["RecommendFamily"])
app.include_router(evaluate.router, prefix="/evaluate", tags=["Evaluate"])
app.include_router(predict.router, prefix="/predict", tags=["Predict"])

# Ruta raíz
@app.get("/")
async def read_root():
    return {"message": "Welcome to the persistence module of the Metabolite Separation API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)