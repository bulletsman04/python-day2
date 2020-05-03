from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def hello_world():
    return {"msg": "Hello world"}

class HelloNameResp(BaseModel):
    msg: str

@app.get('/hello/{name}', response_model=HelloNameResp)
def hello_name(name: str):
    return HelloNameResp(msg=f"Hello {name}")
