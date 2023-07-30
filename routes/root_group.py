from sanic import Blueprint

from routes.analyse import analyse
from routes.stocks import stocks

root_group = Blueprint.group(stocks, analyse, version=1, url_prefix="/")
