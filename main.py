import urllib
import os
import math

host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'fa_kassa')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'root')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode', 'prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server,
                                                               db_server_port, database_name, ssl_mode)

import sqlalchemy

metadata = sqlalchemy.MetaData()

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column("quantity", sqlalchemy.Integer),
    sqlalchemy.Column("percent", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=10, max_overflow=0
)

metadata.create_all(engine)

from pydantic import BaseModel
from datetime import datetime

class ProductIn(BaseModel):
    name: str
    text: str
    percent: int = None
    price: float
    quantity: int


class Products(BaseModel):
    id: int
    name: str
    text: str
    # image:
    percent: int = None
    price: float
    quantity: int
    date: datetime

from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI(title="using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

import databases
from sqlalchemy.orm import Session

database = databases.Database(DATABASE_URL)

from starlette.requests import Request


def get_db(request: Request):
    return request.state.db

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/prod", response_model=List[Products])
async def list_prod(product: Session = Depends(get_db)):
    return list_prod(product)


@app.post("/prod", response_model=Products)
async def create_prod(product: ProductIn = File(...)):
    query = products.insert().values(text=product.name)
    last_record_id = await database.execute(query)
    # product_dict = product.dict()
    # if product.percent:
    #     price_with_percent = product.price + (product.percent*0.01)
    #     product_dict.update({"price_with_percent": price_with_percent})
    return {**product.dict(), "id": last_record_id}
