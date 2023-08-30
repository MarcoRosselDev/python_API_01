from fastapi import FastAPI, Body, Response, status, HTTPException
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
        
def found_id(id): 
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}

@app.get("/myposts")
def myposts():
    return {'data': my_posts }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(x_var_name: Post ):
    #x_var_name = dict(x_var_name)
    post_dict = dict(x_var_name)
    post_dict['id'] = int(random.randint(0, 1000))
    my_posts.append(post_dict)
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_one_post(id:int):
    post =  get_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {'post_detail': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    index = found_id(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, x_post:Post):
    index = found_id(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
    post_dict = x_post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'data': post_dict}