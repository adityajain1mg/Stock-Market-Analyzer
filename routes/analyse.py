from sanic import Blueprint, json
from sanic.response import text
from sanic_ext import render

from managers.analyse import compare_data, historical_data, real_time_data

analyse = Blueprint('analyse', version=1, url_prefix="/analyse")


@analyse.route("/", methods=['GET'])
async def show(request):
    return text("Analyse Blueprint Root")


@analyse.route("/home", methods=['GET'])
async def get_home(request):
    return await render("home.html", status=200)


@analyse.route("/historical-analysis", methods=['GET'])
async def historical_analysis_get(request):
    return await render("historical.html", status=200)


@analyse.route("/historical-analysis", methods=['POST'])
async def historical_analysis_post(request):
   return await historical_data(request)


@analyse.route("/compare", methods=['GET'])
async def compare_get(request):
    return await render("compare.html", status=200)


@analyse.route("/compare", methods=['POST'])
async def compare_post(request):
    return await compare_data(request)


@analyse.route("/real-time", methods=['GET'])
async def real_time(request):
    return await render(
        "real_time.html", status=200
    )


@analyse.route("/real-time", methods=['POST'])
async def real_time_post(request):
    return await real_time_data(request)
