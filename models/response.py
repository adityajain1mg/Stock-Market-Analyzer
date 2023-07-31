from dataclasses import dataclass
from sanic_ext import render
from managers.stock_manager import StockManager
@dataclass
class Response:
    html: str
    context: dict
    status: int

    @classmethod
    async def get_response(cls, Request, template):
        stock = Request.stock
        if Request.duration is None and Request.candle_size is None:
            return await render(
                template, context={"data": {"stock": stock[0]}}, status=200
            )

        return await StockManager.analysis_manager(Request, template)

