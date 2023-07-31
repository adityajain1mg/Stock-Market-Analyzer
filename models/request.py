from attr import validate
from pydantic import BaseModel
from pydantic import validator


class Request(BaseModel):
    stock: list
    duration: str
    candle_size: str

    @validator('duration', 'candle_size', pre=True)
    def convert_to_single_value(cls, value):
        return value[0] if isinstance(value, list) else value

    # @classmethod
    # def from_request(cls, request):
    #     args = request.args
    #     return cls(
    #         stock=args.getlist('stock'), 
    #         duration=args.get('duration'), 
    #         candle_size=args.get('candle-size'))
