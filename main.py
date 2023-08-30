from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional

my_posts = [{'title':'my first post', 'content': 'content of my first post', 'id': 1}, {'title':'my second post', 'content': 'content of my second post', 'id': 2}]

def get_post(id):
    for i in my_posts:
        if i['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}

@app.get("/myposts")
def myposts():
    return {'data': my_posts }

@app.post("/posts")
def create_posts(x_var_name: Post ):
    #x_var_name = dict(x_var_name)
    post_dict = dict(x_var_name)
    post_dict['id'] = int(random.randint(0, 1000))
    my_posts.append(post_dict)
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_one_post(id:int):
    resp =  get_post(id)
    return {'post_detail': resp}