from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Dict, Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no se encontró. Asegúrate de que el archivo .env esté configurado.")
    
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/inicio", scheme_name="JWTAuth") 


def create_access_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_payload(token: Annotated[str, Depends(oauth2_scheme)]):

    try:
        print(f"\n[DEBUG VALIDADOR] Clave de verificación: '{SECRET_KEY}'")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id_cliente = payload.get("id_cliente")

        if id_cliente is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: falta id_cliente.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload 

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )