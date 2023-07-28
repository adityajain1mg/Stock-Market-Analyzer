from sanic import Sanic, json
from sanic.response import text 

from routes.root_group import root_group

app = Sanic("StockAnalyser")

app.blueprint(root_group)

@app.get("/")
async def hello_world(request):
    return json({"msg":"Stock Market Analyzer - Aditya Jain"})

@app.get("/help")
async def help(request):
    return json({"help": "Help is on the way"})

if __name__ == '__main__':
    app.run()