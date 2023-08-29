from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional

my_posts = [{'title':'my first post', 'content': 'content of my first post', 'id': 1}, {'title':'my second post', 'content': 'content of my second post', 'id': 2}]

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}

@app.get("/myposts")
def myposts():
    return {'posts': my_posts }

@app.post("/posts")
def create_posts(x_var_name: Post ):
    x_var_name = dict(x_var_name)
    x_var_name['id'] = 76152
    my_posts.append(x_var_name)
    return {"title": my_posts}