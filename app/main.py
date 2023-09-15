from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from .routers import user, post, auth

from decouple import config # .env config
pass_sql = config('MY_PSQL_PASS') # sintaxis para guardar los pass seguros
import time # to sleep 2 second to retry connect with database
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}
