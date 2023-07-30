from sanic.exception import BadRequest
class ValidateData:
    @classmethod
    def validate(cls, request):
        if request.args is None or len(request.args) != 3:
            raise BadRequest("Missing Data")

        stock = request.args.getlist('stock')
        if request.path == '/v1/analyse/historical':
            if stock is None or len(stock) != 1:
                raise BadRequest("Missing Stock Data")
        elif request.path == '/v1/analyse/compare':
            if stock is None or len(stock) != 2:
                raise BadRequest("Missing Stock Data")
        if cls.validate_data(request):
            return True
        return False

    @classmethod
    def validate_data(cls, request):
        duration = request.args.get('duration')
        candle_size = request.args.get('candle-size')

        if duration is None or duration not in ['1D', '1M', '3M', '6M', '1Y']:
            raise BadRequest("Duration is either missing or incorrect duration is provided")
        elif candle_size is None or candle_size not in ['1min', '5min', '15min', '1D', '1M']:
            raise BadRequest("Candle size is either missing or incorrect candle size is provided")

        return True


def validate_data(func):
    @wraps(func)
    async def decorated_function(request, *args, **kwargs):
        args = request.args
        if args is None:
            raise BadRequest("Missing query parameters")
        else:
            stock = args.getlist('stock')
            duration = args.get('duration')
            candle_size = args.get('candle-size')

            if request.path == '/v1/analyse/realtime':
                if stock is None or len(stock) != 1:
                    raise BadRequest("Invalid Data")
            else:
                if request.path == '/v1/analyse/historical':
                    if stock is None or len(stock) != 1:
                        raise BadRequest("Invalid Data")
                else:
                    if stock is None or len(stock) != 2:
                        raise BadRequest("Invalid data")
                
                if duration is None or duration not in ['1D', '1M', '3M', '6M', '1Y']:
                    raise BadRequest("Duration is either missing or incorrect duration is provided")
                elif candle_size is None or candle_size not in ['1min', '5min', '15min', '1D', '1M']:
                    raise BadRequest("Candle size is either missing or incorrect candle size is provided")   
        return await func(request, *args, **kwargs)

    return decorated_function
