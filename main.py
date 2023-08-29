from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Worlddddd"}

@app.get("/home")
def home_page():
    return {'home page': 'some page in the future'}

@app.post("/createposts")
def create_posts(x_var_name: dict = Body(...) ):
    print(x_var_name)
    return {f"{x_var_name['title']}": f"body : {x_var_name['body']}"}