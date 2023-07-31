from sanic import Blueprint, json
from sanic.response import text

from managers.validate_manager import ValidateData
from managers.stocks import StockDb

stocks = Blueprint('stock_list', version = 1,  url_prefix="/stocks")

@stocks.get("/")
async def show(request):
    return text("Stocks Blueprint Root")

@stocks.get("/show-list")
async def show_list(request):

    rows = await StockDb.read_stock()
    return json({"stock_list": rows})

@stocks.post("/add-stock")
async def add_stock(request):
    ValidateData.validate_body(request)
    body = request.json  
    result = await StockDb.add_stock(body['stock_name'])

    return json({"msg": result})

@stocks.post("/remove-stock")
async def remove_stock(request):
    ValidateData.validate_body(request)
    body = request.json
    result = await StockDb.remove_stock(body['stock_name'])
    
    return json({"msg": result})
