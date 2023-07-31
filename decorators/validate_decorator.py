from functools import wraps
from logging import log
from sanic.log import logger
from sanic.exceptions import BadRequest

def validate(x):
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            logger.info("decorator start")
            query_args = request.args
            stock = query_args.getlist('stock')
            duration = query_args.get('duration')
            candle_size = query_args.get('candle_size')

            if stock is None or len(stock) != x:
                raise BadRequest("Incorrect amount of stock symbol provided")
            if duration is None or duration not in ['1D', '1M', '3M', '6M', '1Y']:
                raise BadRequest("Duration is either missing or incorrect duration is provided")
            elif candle_size is None or candle_size not in ['1min', '5min', '15min', '30min', '60min', '1D']:
                raise BadRequest("Candle size is either missing or incorrect candle size is provided")  

            logger.info("decorator end") 
            return await func(request, *args, **kwargs)
        return decorated_function
    return decorator 