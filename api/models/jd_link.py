from typing import List
from pydantic import BaseModel, HttpUrl


class JDLink(BaseModel):
    rel: str
    uri: HttpUrl

