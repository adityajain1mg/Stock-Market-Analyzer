from dataclasses import dataclass

@dataclass
class Request:
    stock: list(str)
    duration: str
    candle_size: str
    
    @classmethod
    def from_request(cls, request):
        args = request.args
        return cls(
            stock=args.getlist('stock'), 
            duration=args.get('duration'), 
            candle_size=args.get('candle-size'))
