from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}

@app.get("/home")
def home_page():
    return {'home page': 'some page in the future'}

@app.post("/createposts")
def create_posts(x_var_name: Post ):
    print(x_var_name)
    print(x_var_name.published)
    return {"title": "body response"}