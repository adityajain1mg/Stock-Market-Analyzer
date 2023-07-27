from sanic import Blueprint, json
from sanic.response import text
from sanic_ext import render

from managers.stocks import read_stock, add_stock, remove_stock, update_preferences, get_preferences
from managers.analyse import analysis_manager, compare_data, historical_data, real_time_data

analyse = Blueprint('analyse', version=1, url_prefix="/analyse")


@analyse.get("/")
async def show(request):
    return text("Analyse Blueprint Root")


@analyse.get("/home")
async def get_home(request):
    return await render("home.html", status=200)


@analyse.get("/historical-analysis")
async def historical_analysis_get(request):
    return await render("historical.html", status=200)


@analyse.post("/historical-analysis")
async def historical_analysis_post(request):
   return await historical_data(request)


@analyse.get("/compare")
async def compare_get(request):
    return await render("compare.html", status=200)


@analyse.post("/compare")
async def compare_post(request):
    return await compare_data(request)


@analyse.get("/real-time")
async def real_time(request):
    return await render(
        "real_time.html", status=200
    )


@analyse.post("/real-time")
async def real_time_post(request):
    return await real_time_data(request)
