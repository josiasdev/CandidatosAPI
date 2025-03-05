from pymongo import MongoClient
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.accidents import router as accidents_router
from routes.BensCandidato import router as bens_candidato_router
from routes.Candidatura import router as candidatura_router
import logging
from logging.handlers import RotatingFileHandler

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Configuração de logs
LOG_FILE = "app.log"
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Recebendo requisição: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Resposta gerada com status: {response.status_code}")
    return response

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient("mongodb://localhost:27017")
    app.database = app.mongodb_client['Candidatos']
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print("Disconnected to the MongoDB database!")

@app.get("/")
async def homepage():
    logger.info("Endpoint /hello-world acessado")
    return {"message": "welcome to our homepage"}

app.include_router(accidents_router, prefix="/accidents", tags=["Accidents"])
app.include_router(bens_candidato_router, prefix="/bens_candidato", tags=["BensCandidato"])
app.include_router(candidatura_router, prefix="/candidatura", tags=["Candidatura"])