from attr import validate
from pydantic import BaseModel
from pydantic import validator
from sanic.exceptions import BadRequest


class Request(BaseModel):
    stock: list
    duration: str
    candle_size: str

    @validator('duration', 'candle_size', pre=True)
    def convert_to_single_value(cls, value):
        return value[0] if isinstance(value, list) else value

    @validator('duration')
    def duration_from_list(cls, duration):
        durations = ['1D', '1M', '3M', '6M', '1Y']
        if duration not in durations:
            raise ValueError("Duration is either missing or incorrect duration is provided")
        return duration
    
    @validator('candle_size')
    def candle_size_from_list(cls, candle_size):
        candle_sizes = ['1min', '5min', '15min', '30min', '60min', '1D']
        if candle_size not in candle_sizes:
            raise ValueError("Invalid candle size")

    # @classmethod
    # def from_request(cls, request):
    #     args = request.args
    #     return cls(
    #         stock=args.getlist('stock'), 
    #         duration=args.get('duration'), 
    #         candle_size=args.get('candle-size'))
