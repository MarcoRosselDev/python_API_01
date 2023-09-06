from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from decouple import config # .env config
secret_key_env = config('SECRET_KEY')
algorithm_env = config('ALGORITHM')

# secret key
# algorithm
# expiration time

SECRET_KEY = secret_key_env
ALGORITHM = algorithm_env
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id_user:str = payload.get("user_id")
        if id_user is None:
            raise credentials_exeption
        token_data = schemas.TokenData(id_user=id)
    except JWTError:
        raise credentials_exeption