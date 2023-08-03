from sanic import Blueprint, json
from sanic.response import text
from decorators.validate_decorator import validate_body
from managers.stocks import StockDb

stocks = Blueprint('stock_list', version = 1,  url_prefix="/stocks")

@stocks.get("/")
async def show(request):
    return json({"msg": "Stocks Blueprint Root"})

@stocks.get("/show-list")
async def show_list(request):

    rows = await StockDb.read_stock()
    return json({"stock_list": rows})

@stocks.post("/add-stock")
@validate_body
async def add_stock(request):
    body = request.json  
    result = await StockDb.add_stock(body['stock_name'])

    return json({"msg": result})

@stocks.post("/remove-stock")
@validate_body
async def remove_stock(request):
    body = request.json
    result = await StockDb.remove_stock(body['stock_name'])
    
    return json({"msg": result})
