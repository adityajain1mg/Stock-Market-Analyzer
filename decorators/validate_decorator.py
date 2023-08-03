from functools import wraps
from logging import log
from sanic.log import logger
from sanic.exceptions import BadRequest

def validate(stock_count):
    def decorator(func):
        @wraps(func)
        async def decorated_function(request, *args, **kwargs):
            query_args = request.args
            stock = query_args.getlist('stock')

            if stock is None or len(stock) != stock_count:
                raise BadRequest("Incorrect amount of stock symbol provided")

            return await func(request, *args, **kwargs)
        return decorated_function
    return decorator 

def validate_realtime(func):
    @wraps(func)
    async def decorated_function(request, *args, **kwargs):
        query_args = request.args
        stock = query_args.getlist('stock')
        if len(query_args) != 1 or len(stock) != 1:
            raise BadRequest("Invalid Data Provided")
        return await func(request, *args, **kwargs)

    return decorated_function


def validate_body(func):
    @wraps(func)
    async def decorated_function(request, *args, **kwargs):
        body = request.json
        if body is None:
            raise BadRequest("Data not provided")
        if len(body.keys()) != 1 or body.get('stock_name') is None:
            raise BadRequest("Invalid data provided")
        if not isinstance(body.get('stock_name'), str):
            raise BadRequest("Stock should not be in a list")
        return await func(request, *args, **kwargs)
    return decorated_function