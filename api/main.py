from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import ecs

app = FastAPI()

# TODO: find out about stricter deserialization & validation constraints
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
# TODO: make this an ECS metadata passthrough
def read_root():
    # return {"Hello": "World"}
    ecs.get_task_metadata()  # config file or docker container setting to make this work in one form or another locally - like a local json file ? 

# TODO: copilot & working with secrets (copilot addons ? )
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