from sanic import Sanic, json
from routes.root_group import root_group
from common import help
app = Sanic("StockAnalyser")
app.config.FALLBACK_ERROR_FORMAT = "json"
app.blueprint(root_group)

@app.get("/")
async def get_page(request):
    return redirect('/help')

@app.get("/help")
async def get_help(request):
    return json(help)

if __name__ == '__main__':
    app.run()