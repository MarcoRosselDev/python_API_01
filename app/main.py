from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers import user, post

from decouple import config # .env config
pass_sql = config('MY_PSQL_PASS') # sintaxis para guardar los pass seguros
import time # to sleep 2 second to retry connect with database
app = FastAPI()

""" class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional """
    
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fast_api_01', user='postgres', password=pass_sql, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Databese connection was successfull')
        break
    except Exception as error:
        print('Connecting to database failed')
        print('Error: ', error)
        time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}
