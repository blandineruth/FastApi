from typing import List, Dict
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String  
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from datetime import datetime


DATABASE_URL = "sqlite:///./db_test.db"

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

register = Table(
    "register",
    metadata,
    sqlalchemy.Column ("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column ("name", sqlalchemy.String(500)),
    sqlalchemy.Column ("date_create", sqlalchemy.DateTime())
)

engine = sqlalchemy.create_engine(
DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def connect():
    await database.disconnect()

class Register():
    id: int
    name:str
    date_created : datetime

class registerIn(BaseModel):
    name : str = Field(...)

@app.post("/register/", response_model=Dict[str, str])
async def create(r: registerIn = Depends()):
    query = register.insert().values(
        name = r.name,
         date_created = datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return dict(row) 

@app.get("/register/{id}", response_model=Register)
async def get_one(id: int):
    query = register.select().where(register.c.id == id)
    user = await database.fetch_one(query)
    return dict(user)

@app.get("/register/", response_model=List[Register])
async def get_all():
    query= register.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.put("/register/{id}", response_model=Register)
async def update(id: int, r: registerIn = Depends()):
    query = register.update().where(register.c.id == id).values(
        name = r.name,
        date_created= datetime.utcnow()
    )
    record_id = await database.excute(query)
    query = register.select().where(register.c.id == record_id)
    row =await database.fect_one(query)
    return dict(row)

@app.delete("/register/{id}", response_model=Register)
async def delete(id: int):
    query =  register.delete(). where(register.c.id == id)
    return await database.execute(query)