from sanic_ext import render

from managers.api_manager import StockDataApi
from managers.stocks import StockDb
from models.response import Response


class StockManager:
    @classmethod
    async def analysis(cls, Request, template):
        """It analysis the stock_list to get the data from the api_call
        and process that data and display the data inside a rendered html page.

        Args:
            request (_type_): request from the form
            template (html): html page to be rendered
        """
        stock_list = Request.stock
        candle_size = Request.candle_size
        duration = Request.duration

        previous_stocks = await StockDb.read_stock()

        stock_data = []
        for stock in stock_list:
            historical_data = await cls.get_historical_data_df(candle_size, duration, stock)
            # stock = Stock(**historical_data)
            await StockDb.add_stock(stock.upper())
            stock_data.append(historical_data)
        response_dict = {
            "data":{
                "template": template, 
                "context": {
                    "stock_data": stock_data,
                    "previous_stocks": previous_stocks
                }
            },
            "status_code":200,
            "message" : "Data is provided"
        }

        responseObject = Response(**response_dict)

        return await render(
            responseObject.data["template"],
            context=responseObject.data["context"],
            status=responseObject.status_code
        )

    @classmethod
    async def _get_historical_data_df(cls, candle_size, duration, stock):
        """ 
        Calculate Avg, Max, Min, Moving Average, RSI form the api call data.

        Args:
            candle_size (str): duration between two datapoints
            duration (str): time period of data
            stock (str): stock sybol

        Returns:
            dict: dictionary of data
        """

        data_df = await StockDataApi.api_data(stock, duration, candle_size)

        data_df['MA'] = data_df['4. close'].rolling(window=7, min_periods=1).mean()
        data_df['RSI'] = await cls.calculate_rsi(data_df['4. close'])
        data_df['RSI'] = data_df['RSI'].fillna(0)
        data_df['MA'] = data_df['MA'].fillna(0)

        min_close = data_df['4. close'].min()
        max_close = data_df['4. close'].max()
        avg_close = data_df['4. close'].mean()

        stock_data = {
            "symbol": stock,
            "date": data_df.index.tolist(),
            "close": data_df['4. close'].tolist(),
            "min": float(min_close),
            "max": float(max_close),
            "average": float(avg_close),
            "ma": data_df['MA'].tolist(),
            "rsi": data_df['RSI'].tolist()
        }
        return stock_data

    @classmethod
    async def _calculate_rsi(cls, prices, period=14):
        """Calculate RSI using api-call data

        Args:
            prices (dataframe): dataframe of closing prices
            period (int, optional): period of rolling back. Defaults to 14.

        Returns:
            dataframe : dataframe of RSI values
        """
        delta = prices.diff().dropna()
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        avg_gains = gains.rolling(window=period, min_periods=1).mean()
        avg_losses = losses.rolling(window=period, min_periods=1).mean()
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        return rsi


