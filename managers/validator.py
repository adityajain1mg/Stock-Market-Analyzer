from sanic.exceptions import BadRequest


class ValidateData:

    @classmethod
    def validate_data_historical(cls, request):

        if request.args is None or len(request.args) != 3:
            raise BadRequest("Missing Data")

        stock = request.args.get('stock')
        if stock is None:
            raise BadRequest("Missing Stock Data")

        if cls.validate_data(request):
            return True
        return False

    @classmethod
    def validate_data_compare(cls, request):
        if request.args is None or len(request.args) != 3:
            raise BadRequest("Missing Data")

        stock = request.args.getlist('stock')
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
