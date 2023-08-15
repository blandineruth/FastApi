from fastapi import FastAPI
import uvicorn
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class CoordIn(BaseModel):
    password:str
    lat: float
    lon: float
    zoom: Optional[int] =  None

class CoordOut(BaseModel):
    lat: float
    lon: float
    zoom: Optional[int] =  None

#get,Put,delete

@app.get("/")
async def hello_word():
    return{"Hello": "word"}

@app.post("/position/", response_model=CoordOut)
async def make_position(coord:CoordIn):
    #db write completed
    return coord




































# @app.get("/component/{component_id}") #path parameter
# async def get_component(component_id:int):
#     return {"component_id" : component_id}

@app.get("/component/")
async def read_component(number:int, text:str):
    return{ "number": number, "text": text}

# http://http://127.0.0.1:8000/component/?number=12&text=component


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)