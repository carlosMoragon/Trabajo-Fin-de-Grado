'''from fastapi import FastAPI
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
    uvicorn.run(app, host="0.0.0.0", port=8010)'''
from fastapi import FastAPI, Request
from routes import experiments, families, feedback, recommendFamily, evaluate, predict
import logging
import uvicorn
import time

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Middleware para loguear todas las peticiones (incluso las que fallan validación)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Leemos el body completo
    body_bytes = await request.body()
    # Creamos un receive que devuelva de nuevo el mismo body
    async def receive() -> dict:
        return {"type": "http.request", "body": body_bytes}

    # Reconstruimos la Request con el body preservado
    request = Request(request.scope, receive)

    start_time = time.time()
    response = await call_next(request)
    elapsed = (time.time() - start_time) * 1000

    # Imprimimos info de la petición
    logger.info(f"➡️ {request.method} {request.url.path} completed_in={elapsed:.2f}ms status_code={response.status_code}")
    logger.info(f"Headers: {dict(request.headers)}")
    try:
        logger.info(f"Body: {body_bytes.decode('utf-8')}")
    except Exception:
        logger.info(f"Body (bytes): {body_bytes}")

    return response

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
