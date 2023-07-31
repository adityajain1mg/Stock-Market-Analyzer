from sanic import Blueprint, json
from sanic.response import text
from sanic_ext import render
from decorators.validation_decorator import validate_query
from models.request import Request
from models.response import Response
analyse = Blueprint('analyse', version=1, url_prefix="/analyse")


@analyse.get("/historical")
@validate_query
async def get_historical(request):
    args = request.args
    request_call = Request(**args)
    return await Response.get_response(request_call, "historical_data.html")


@analyse.get("/compare")
@validate_query
async def get_compare(request):
    args = request.args
    request_call = Request(**args)
    return await Response.get_response(request_call, "compare_data.html")


@analyse.get("/realtime")
@validate_query
async def get_realtime(request):
    args = request.args
    request_call = Request(**args)
    return await Response.get_response(request_call, "real_time_data.html")