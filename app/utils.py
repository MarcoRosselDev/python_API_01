from passlib.context import CryptContext # algorithm to encript our user passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str):
    return pwd_context.hash(password)