from functools import wraps

from sanic.exceptions import BadRequest


def validate_query(func):
    @wraps(func)
    async def decorated_function(request, *args, **kwargs):
        query_args = request.args
        if query_args is None:
            raise BadRequest("Missing query parameters")
        else:
            stock = query_args.getlist('stock')
            duration = query_args.get('duration')
            candle_size = query_args.get('candle_size')

            if request.path == '/v1/analyse/realtime':
                if stock is None or len(stock) != 1:
                    raise BadRequest("Incorrect amount of stock symbol provided")
                elif duration is not None or candle_size is not None:
                    raise BadRequest("Invalid data provided")
            else:
                if request.path == '/v1/analyse/historical':
                    if stock is None or len(stock) != 1:
                        raise BadRequest("Incorrect amount of stock symbol provided")
                else:
                    if stock is None or len(stock) != 2:
                        raise BadRequest("Incorrect amount of stock symbol provided")
                
                if duration is None or duration not in ['1D', '1M', '3M', '6M', '1Y']:
                    raise BadRequest("Duration is either missing or incorrect duration is provided")
                elif candle_size is None or candle_size not in ['1min', '5min', '15min', '30min', '60min', '1D']:
                    raise BadRequest("Candle size is either missing or incorrect candle size is provided")   
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


# class ValidateData:

#     @classmethod
#     def validate(cls, request):
#         if request.args is None or len(request.args) != 3:
#             raise BadRequest("Missing Data")

#         stock = request.args.getlist('stock')
#         if request.path == '/v1/analyse/historical':
#             if stock is None or len(stock) != 1:
#                 raise BadRequest("Missing Stock Data")
#         elif request.path == '/v1/analyse/compare':
#             if stock is None or len(stock) != 2:
#                 raise BadRequest("Missing Stock Data")
#         if cls.validate_data(request):
#             return True
#         return False

#     @classmethod
#     def validate_data(cls, request):
#         duration = request.args.get('duration')
#         candle_size = request.args.get('candle-size')

#         if duration is None or duration not in ['1D', '1M', '3M', '6M', '1Y']:
#             raise BadRequest("Duration is either missing or incorrect duration is provided")
#         elif candle_size is None or candle_size not in ['1min', '5min', '15min', '1D', '1M']:
#             raise BadRequest("Candle size is either missing or incorrect candle size is provided")

#         return True

