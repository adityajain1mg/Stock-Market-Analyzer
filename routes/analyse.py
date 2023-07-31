from sanic import Blueprint, json
from sanic.response import text
from sanic_ext import render
from decorators.validate_decorator import validate
from managers.validate_manager import ValidateData
from models.request import Request
from models.response import Response
from managers.stock_manager import StockManager
analyse = Blueprint('analyse', version=1, url_prefix="/analyse")


@analyse.get("/historical")
@validate(x=1)
async def get_historical(request):
    args = request.args
    requestObject = Request(**args)
    # ValidateData.validate(request, requestObject)
    return await StockManager.analysis(requestObject, "historical_data.html")


@analyse.get("/compare")
@validate(x=2)
async def get_compare(request):
    args = request.args
    requestObject = Request(**args)
    return await StockManager.analysis(requestObject, "compare_data.html")


@analyse.get("/realtime")
async def get_realtime(request):
    ValidateData.validate_realtime(request)
    stock = request.args.get('stock')
    return await render(
                "real_time_data.html", context={"data": {"stock": stock}}, status=200
            )