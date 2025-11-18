from datetime import datetime, timedelta
from jose import jwt

# Clave secreta para firmar el token (colócala en .env más adelante)
SECRET_KEY = "CLAVE_SECRETA_SUPER_SEGURA"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    """
    Genera un token JWT usando los datos enviados.
    Se agrega fecha de expiración automáticamente.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
