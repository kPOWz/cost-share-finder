from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
import api.ecs as ecs

app = FastAPI()

# TODO: find out about stricter deserialization & validation constraints
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root(request : Request):
    # return {"Hello": "World"}
    return ecs.get_task_metadata()

# TODO: oauth 2 authorization flow request
# TODO: oauth 2 callback
# TODO: oauth 2 current user endpoint
# TODO: oauth refresh token 

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "is_offer": item.is_offer}