from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
import api.ecs as ecs
from .routers import oauth2_client

app = FastAPI()
# TODO: pull out a few things as config/settings & add https_only true (false forlocal only) , same_site='Strict'
app.add_middleware(SessionMiddleware, secret_key="secret-string", max_age=60 * 2)
app.include_router(oauth2_client.router)

# TODO: find out about stricter deserialization & validation constraints
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root():
    # return {"msg": "Hello World"}
    return ecs.get_task_metadata()

# TODO: test jd auth flow from ECS  - need envirionment vars added
# TODO: need addtional env vars for security measures on SessionMiddleware setup oauthlib insecure transport,etc...
# TODO: need a pipeline (via copilot)
# TODO: oauth refresh token
# TODO: FastAPI Depends
# TODO: async/await 
# TODO: FastAPI / Pydantic Settings/Config  - need to clean up a whole bunch of settings

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "is_offer": item.is_offer}