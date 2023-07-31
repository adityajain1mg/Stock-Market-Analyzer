
from sanic.log import logger
from sanic.exceptions import BadRequest

class ValidateData:

    @classmethod
    def validate_realtime(cls, request):
        args = request.args
        logger.info(len(args))
        stock = args.getlist('stock')
        if len(args) != 1 or len(stock) != 1:
            raise BadRequest("Invalid Data Provided")
        return None

    @classmethod
    def validate_body(cls, request):
        body = request.json
        if body is None:
            raise BadRequest("Data not provided")
        if len(body.keys()) != 1 or body.get('stock_name') is None:
            raise BadRequest("Invalid data provided")
        if not isinstance(body.get('stock_name'), str):
            raise BadRequest("Stock should not be in a list")
        return None