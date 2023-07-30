from managers.api_manager import StockDataApi
from managers.validator import ValidateData
from managers.stocks import read_stock, add_stock
import datetime
from dateutil.relativedelta import relativedelta
from sanic_ext import render
from sanic.response import text
from utils import break_string
import pandas as pd

class StockManager:
    @classmethod
    async def historical_data(cls, request):
        """
        Rendering historical data page using the incoming form data
        """
        if ValidateData.validate_data_historical(request):
            return await cls.analysis_manager(request, "historical_data.html")
        else:
            raise "Invalid data provided"

    @classmethod
    async def compare_data(cls, request):
        """
        Rendering compare data page using the incoming form data
        """
        if ValidateData.validate_data_compare(request):
            return await cls.analysis_manager(request, "compare_data.html")
        else:
            raise "Invalid data provided"

    @classmethod
    async def real_time_data(cls, request):
        """
        Rendering real time data page using the incoming form data
        """
        stock = request.args.get('stock')
        return await render(
            "real_time_data.html", context={"data": {"stock": stock}}, status=200
        )

    @classmethod
    async def analysis_manager(cls, request, template):
        """It analysis the stock_list to get the data from the api_call
        and process that data and display the data inside a rendered html page.

        Args:
            request (_type_): request from the form
            stock_list (list): list of stocks 
            template (html): html page to be rendered
        """
        stock_list = request.args.getlist('stock')
        previous_stocks = await read_stock()


        candle_size = request.args.get('candle-size')
        duration = request.args.get('duration')

        stock_data = []

        for stock in stock_list:

            success, historical_data = await cls.get_historical_data_df(candle_size, duration, stock)

            if not success:
                return text("Something Went Wrong :( \nRefer to the below message\n" + str(historical_data))

            await add_stock(stock)
            stock_data.append(historical_data)

        return await render(
            template,
            context={
                "stock_data": stock_data,
                "preferences": [candle_size, duration],
                "previous_stocks": previous_stocks
            },
            status=200
        )

    @classmethod
    async def get_historical_data_df(cls, candle_size, duration, stock):
        """ 
        Calculate Avg, Max, Min, Moving Average, RSI form the api call data.

        Args:
            candle_size (str): duration between two datapoints
            duration (str): time period of data
            stock (str): stock sybol

        Returns:
            dict: dictionary of data
        """
        # candle_size_prefix, candle_size_suffix = break_string(candle_size)

        # function_type = period_function_mapping.get(candle_size_suffix, "TIME_SERIES_DAILY")
        # symbol = stock
        # interval = candle_size
        # url = URL.format(function_type, symbol, interval, ALPHA_VANTAGE_API_KEY)
        # try:
        #     res = await make_request(url)
        # except Exception as e:
        #     return False, str(e)

        res = await StockDataApi.api_data(stock, duration, candle_size)
        time_series_data = None

        for key in list(res.keys()):
            if "Time Series" in key:
                time_series_data = res[key]

        if time_series_data is None:
            message = str(res)
            print(message)
            return False, message

        data = res[list(res.keys())[1]]
        data_df = pd.DataFrame(data).T

        today_date = datetime.datetime.now().date()
        duration_prefix, duration_suffix = break_string(duration)
        final_date = today_date
        if duration_suffix == 'Y':
            final_date -= relativedelta(years=1)
        else:
            final_date -= relativedelta(months=int(duration_prefix))

        start_date = final_date.strftime('%Y-%m-%d')
        end_date = today_date.strftime('%Y-%m-%d')
        data_df['4. close'] = data_df['4. close'].astype(float)
        data_df = data_df[::-1]
        # data_df['change'] = data_df['4. close'].pct_change().fillna(0)
        # data_df.to_csv("historical.csv")
        data_df['MA'] = data_df['4. close'].rolling(window=7, min_periods=1).mean()
        data_df['RSI'] = await cls.calculate_rsi(data_df['4. close'])
        data_df['RSI'] = data_df['RSI'].fillna(0)
        data_df['MA'] = data_df['MA'].fillna(0)

        data_df = data_df.loc[(data_df.index >= start_date) & (data_df.index <= end_date)]
        min_close = data_df['4. close'].min()
        max_close = data_df['4. close'].max()
        avg_close = data_df['4. close'].mean()

        stock_data = {
            "symbol": stock,
            "labels": data_df.index.tolist(),
            "closing": data_df['4. close'].tolist(),
            "min": float(min_close),
            "max": float(max_close),
            "average": float(avg_close),
            "ma": data_df['MA'].tolist(),
            "rsi": data_df['RSI'].tolist()
        }
        return True, stock_data

    @classmethod
    async def calculate_rsi(cls, prices, period=14):
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
