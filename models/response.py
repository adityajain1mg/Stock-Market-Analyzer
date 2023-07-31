
from pydantic import BaseModel

class Response(BaseModel):
    template: str
    context: dict
    status: int
