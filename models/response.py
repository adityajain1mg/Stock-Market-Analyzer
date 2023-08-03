
from pydantic import BaseModel

class Response(BaseModel):
    data: dict
    status_code: int
    message: str
