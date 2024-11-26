from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.query import Answers, Answer, QueryBase, QueryCreate
from schemas.coordinate import Coordinate, CoordinateCreate, CoordinateBase, CoordinateUpdate
from schemas.user import UserInterests
from cruds.query import create_query
from cruds.coordinate import create_coordinate
from cruds.auth import authenticate_user, get_token, hash_password, get_token_data, get_token_from_header
from cruds.user import get_user
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime

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


def generate_recommendations(user_interests: UserInterests):
    # Crear la solicitud para Azure OpenAI
    body = {
        "messages": [
            {
                "role": "user",
                "content": f"Recomienda destinos de viaje para alguien interesado en {user_interests.interests}"
            }
        ],
        "max_tokens": 300,
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
        answer = result["choices"][0]["message"]["content"].split("\n* ")
        return {"recommendations": answer}
    except requests.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Error al obtener recomendaciones, error is {e}")

# Endpoint para generar recomendaciones
@router.post("/openai/destinations", response_model=Answers)
def generate_destination_answer(query: QueryBase, db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    token_data = get_token_data(token=token, db=db)
    user_db = get_user(db, user_id=token_data.user_id)
    if user_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Crear la solicitud para Azure OpenAI
    message = f"Recomiendame destinos para viajar que sean de tipo {query.travel_type}, con un presupuesto de {query.budget} dolares y que sea para {query.duration} días. E ideal un clima {query.weather}. Que la respuesta siga el formato de: '* Nombre del destino; latitud; longitud; descripción * Nombre del destino; latitud; longitud; descripción * Nombre del destino; latitud; longitud; descripción'."
    interest = UserInterests(interests=message)

    answers = generate_recommendations(interest)["recommendations"]
    text = ""
    for answer in answers:
        answer_ia = answer.split(";")[3]
        text += " "+answer_ia
    
    new_query = QueryCreate(**query.dict(), ia_answer=text, time_stamp=datetime.now(), user_id=user_db.id)
    db_query = create_query(db, new_query)

    response = []
    
    for answer in answers:
        answer_ia = answer.split(";")[3]
        new_coordinate = CoordinateCreate(latitude=answer.split(";")[1][:-4], longitude=answer.split(";")[2][:-4], query_id=db_query.id, name=answer.split(";")[0], answer = answer_ia)
        db_coordinate = create_coordinate(db, new_coordinate)
        response.append(Answer(answer=answer_ia, latitude = new_coordinate.latitude, longitude = new_coordinate.longitude, name = new_coordinate.name, coordinate_id=db_coordinate.id))

    return Answers(coordinates = response)

# Endpoint para generar recomendaciones cuando es anonimo
@router.post("/destinations_anonymous", response_model=Answer)
def generate_destination_answer(query: QueryBase, db: Session = Depends(get_db)):
    # Crear la solicitud para Azure OpenAI
    message = f"Recomiendame un destino para viajar que sea de tipo {query.travel_type}, con un presupuesto de {query.budget} dolares y que sea para {query.duration} días. E ideal un clima {query.weather}. Que la respuesta siga el formato de: 'Nombre del destino; latitud; longitud; descripción'."
    interest = UserInterests(interests=message)

    answer= generate_recommendations(interest)["recommendations"]
    answer_ia = answer.split(";")[3]

    return Answer(answer=answer_ia, latitude = answer.split(";")[1][:-4], longitude = answer.split(";")[2][:-4], name = answer.split(";")[0])