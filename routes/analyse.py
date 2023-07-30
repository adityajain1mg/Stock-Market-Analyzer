from sanic import Blueprint, json
from sanic.response import text
from sanic_ext import render

from decorators.validation_decorator import validate_query
from managers.stock_manager import StockManager

analyse = Blueprint('analyse', version=1, url_prefix="/analyse")


@analyse.get("/historical")
@validate_query
async def get_historical(request):
    return await StockManager.analysis_manager(request, "historical_data.html")


@analyse.get("/compare")
@validate_query
async def get_compare(request):
    return await StockManager.analysis_manager(request, "compare_data.html")


@analyse.get("/realtime")
@validate_query
async def get_realtime(request):
    stock = request.args.get('stock')
    return await render(
        "real_time_data.html", context={"data": {"stock": stock}}, status=200
    )