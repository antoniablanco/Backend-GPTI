from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from dotenv import load_dotenv

import os
import time
import json
import requests

# Importar los routers de las rutas
from routes.openAi import router as openAiRouter

# Cargo el archivo .env
load_dotenv()

# Creo la API
app = FastAPI()

@app.on_event("startup")
def on_startup():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raiz
@app.get("/")
async def read_root():
    return {"message":"Home page"}

# Incluit los routers
app.include_router(openAiRouter, prefix="/openai")