from pymongo import MongoClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.accidents import router as accidents_router

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

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient("mongodb://localhost:27017")
    app.database = app.mongodb_client['trafficAccidents']
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print("Disconnected to the MongoDB database!")

@app.get("/")
async def homepage():
    return {"message": "welcome to our homepage"}

app.include_router(accidents_router, prefix="/accidents", tags=["Accidents"])