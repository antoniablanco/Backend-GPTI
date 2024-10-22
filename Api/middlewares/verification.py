from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Callable

from schemas.authentication import TokenData
from cruds.auth import get_token_data
from cruds.user import get_users
from database import get_db

class PermissionMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app: Callable):
        super().__init__(app)
        self.permissions_list = ["/user", "/openai", "/query"]

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        
        # Excluir solicitudes preflight OPTIONS
        if request.method == "OPTIONS":
            return await call_next(request)
        
        try:
            for path in self.permissions_list:
                if request.url.path.startswith(path) and not auth_header:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Authorization required"},
                    )
        
        except Exception as e:
            print("Error in middleware: ", e)   
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token or error decoding token"},
            )

        response = await call_next(request)
        return response
