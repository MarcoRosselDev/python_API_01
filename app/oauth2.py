from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from .routers.get_db_fun import get_db
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from decouple import config # .env config
secret_key_env = config('SECRET_KEY')
algorithm_env = config('ALGORITHM')
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

# secret key
# algorithm
# expiration time

SECRET_KEY = secret_key_env
ALGORITHM = algorithm_env
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user:str = payload.get("user_id")
        if id_user is None:
            raise credentials_exeption
        token_data = schemas.TokenData(id_user=id)
    except JWTError:
        raise credentials_exeption
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user