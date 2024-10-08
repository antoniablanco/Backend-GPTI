from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

import os
import requests

# Cargo el archivo .env
load_dotenv()

# Configurar las credenciales de Azure OpenAI
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_ID = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Crear el encabezado de la solicitud
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_OPENAI_API_KEY
}

router = APIRouter()

class UserInterests(BaseModel):
    interests: str

# Endpoint para generar recomendaciones
@router.post("/recommendations")
async def generate_recommendations(user_interests: UserInterests):
    # Crear la solicitud para Azure OpenAI
    body = {
        "messages": [
            {
                "role": "user",
                "content": f"Recomienda destinos de viaje para alguien interesado en {user_interests.interests}"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }

    try:
        # Realizar la solicitud a la API de Azure OpenAI
        response = requests.post(
            f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_ID}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}",
            headers=headers,
            json=body
        )

        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"].split("\n\n2.")[0]
        return {"recommendations": answer}
    except requests.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Error al obtener recomendaciones, error is {e}")
