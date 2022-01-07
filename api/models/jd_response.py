from typing import List
from pydantic import BaseModel
from api.models.jd_link import JDLink

class JDResponse(BaseModel):
    links: List[JDLink]
