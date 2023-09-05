from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from decouple import config # .env config
pass_sql = config('MY_PSQL_PASS') # sintaxis para guardar los pass seguros
import time # to sleep 2 second to retry connect with database

from . import models
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

#conn = psycopg2.connect("dbname=Local server user=postgres")

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


""" class Post(BaseModel):  #---> Modelo imortado de pydantic que valida el formato resivido segun un modelo
    title: str      #----> Valor requerido
    content: str    #----> Valor requerido. Si no esta, lanza error.
    published: bool = True  #----> Valor por defecto.
    reting_optional: Optional[int] = None  #---> Valor opcional """

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    
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

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data':posts}

@app.get("/myposts")
def myposts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(x_var_name: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**x_var_name.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}")
def get_one_post(id:int, db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    #post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {'post_detail': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db: Session = Depends(get_db)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, x_post: Post, db: Session = Depends(get_db)):
    #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (x_post.title, x_post.content, x_post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post = updated_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist.")
    updated_post.update(x_post.dict(), synchronize_session=False)
    db.commit()
    return {'data': updated_post.first()}