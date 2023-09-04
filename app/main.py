from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from decouple import config # .env config
import time # to sleep 2 second to retry connect with database

pass_sql = config('MY_PSQL_PASS') # sintaxis para guardar los pass seguros
#conn = psycopg2.connect("dbname=Local server user=postgres")

app = FastAPI()

""" class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional """

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
"""     id: int
    content_at: str """
    
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

my_posts = [{'title':'my first post', 'content': 'content of my first post', 'id': 1}, {'title':'my second post', 'content': 'content of my second post', 'id': 2}]
        
def found_id(id): 
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}

@app.get("/myposts")
def myposts():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {'data': posts }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(x_var_name: Post ):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (x_var_name.title, x_var_name.content, x_var_name.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_one_post(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
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