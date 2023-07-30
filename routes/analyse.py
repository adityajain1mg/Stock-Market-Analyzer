from sanic import Blueprint, json
from sanic.response import text
from sanic_ext import render

from managers.stock_manager import StockManager
from managers.validator import validate_query
analyse = Blueprint('analyse', version=1, url_prefix="/analyse")


@analyse.get("/historical")
@validate_query
async def get_historical(request):
    return await StockManager.historical_data(request)


@analyse.get("/compare")
@validate_query
async def get_compare(request):
    print(request.path)
    return await StockManager.compare_data(request)


@analyse.get("/realtime")
@validate_query
async def get_realtime(request):
    return await StockManager.real_time_data(request)