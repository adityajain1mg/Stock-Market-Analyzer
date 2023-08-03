from sanic import Blueprint
from sanic_ext import render
from decorators.validate_decorator import validate, validate_realtime
from models.request import Request
from managers.stock_manager import StockManager
analyse = Blueprint('analyse', version=1, url_prefix="/analyse")


@analyse.get("/historical")
@validate(stock_count=1)
async def get_historical(request):
    args = request.args
    requestObject = Request(**args)
    return await StockManager.analysis(requestObject, "historical_data.html")


@analyse.get("/compare")
@validate(stock_count=2)
async def get_compare(request):
    args = request.args
    requestObject = Request(**args)
    return await StockManager.analysis(requestObject, "compare_data.html")


@analyse.get("/realtime")
@validate_realtime
async def get_realtime(request):
    stock = request.args.get('stock')
    return await render(
                "real_time_data.html", context={"data": {"stock": stock}}, status=200
            )