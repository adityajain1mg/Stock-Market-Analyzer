from dataclasses import InitVar
from sanic import Sanic, json, redirect
from sanic.worker.loader import AppLoader
from routes.root_group import root_group
from common import help
from db.db_creation import CreateDB
from tortoise.contrib.sanic import register_tortoise
app = Sanic("StockAnalyser")
app.config.FALLBACK_ERROR_FORMAT = "json"
app.blueprint(root_group)


@app.before_server_start
async def setup(app, loop):
    await CreateDB.init()

@app.get("/")
async def get_page(request):
    return redirect('/help')

@app.get("/help")
async def get_help(request):
    return json(help)

if __name__ == '__main__':
    app.run()