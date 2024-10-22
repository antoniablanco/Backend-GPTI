from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from dotenv import load_dotenv

import os
import time
import json
import requests

# Importar los modelos
from models.user import User
from models.query import Query
from models.coordinate import Coordinate

# Importar los routers de las rutas
from routes.openAi import router as openAiRouter
from routes.user import router as userRouter
from routes.auth import router as authRouter
from routes.query import router as queryRouter

# Middlewares
from middlewares.verification import PermissionMiddleware


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

# Middleware de permisos
app.add_middleware(PermissionMiddleware)

# Ruta raiz
@app.get("/")
async def read_root():
    return {"message":"Home page"}

# Incluir los routers
app.include_router(openAiRouter)
app.include_router(userRouter, prefix="/user")
app.include_router(authRouter, prefix="/auth")
app.include_router(queryRouter, prefix="/query")