import asyncio
import requests
import re
from sanic.exceptions import BadRequest, NotFound
# from common import period_function_mapping
# from utils import  break_string
import datetime
from dateutil.relativedelta import relativedelta

def break_string(x):
    pattern = r'(\d+)(\D+)'
    matches = re.match(pattern, x)
    number = matches.group(1)
    characters = matches.group(2)

    return number, characters

api_list = ["alphavantage", "apistocks"]

apis = {
            "alphavantage":{
                "url": "https://alpha-vantage.p.rapidapi.com/query",
                "headers": {
                    "X-RapidAPI-Key": "7b0d7ffcf5msh2c3d7f26e39db7dp11f4bcjsna643d971a75c",
                    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
                }
            },
            "apistocks": {
                "url": "https://apistocks.p.rapidapi.com/daily",
                "headers": {
                    "X-RapidAPI-Key": "7b0d7ffcf5msh2c3d7f26e39db7dp11f4bcjsna643d971a75c",
                    "X-RapidAPI-Host": "apistocks.p.rapidapi.com"
                }
            }
        }

api_stats = {api: {'success': 0, 'failure': 0} for api in api_list}

class StockDataApi:
    @classmethod
    async def auto_select_api(cls, symbol, duration, candle_size):
        tasks = []
        for api in api_list:
            method = f'call_{api}_api'
            if hasattr(cls, method):
                method_name = getattr(cls, method)
                tasks.append(method_name(symbol, duration, candle_size))
            else: 
                raise NotFound(f'method {method} not found')

        results = await asyncio.gather(*tasks)
        success_rates = {
            api: api_stats[api]['success'] / (api_stats[api]['success'] + api_stats[api]['failure'])
            for api in apis}
        max_rate_api = max(success_rates, key=success_rates.get)

        method = f'call_{max_rate_api}_api'
        method_name = getattr(cls, method)
        data = await method_name(symbol, duration, candle_size)
        return data

    @classmethod
    async def call_api(cls, api, url, headers, querystring):
        try:
            res = requests.get(url, headers=headers, params=querystring)
            api_stats[api]["success"] += 1
            response = res.json()
            if len(response.keys()) == 1:
                raise BadRequest(response)
            return response
        except Exception as e:
            api_stats[api]["failure"] += 1
            raise BadRequest(e)

    @classmethod
    async def call_alphavantage_intraday_api(cls, symbol, candle_size):
        print(apis)
        api_name = "alphavantage"
        url = apis[api_name]["url"]
        headers = apis["alphavantage"]["headers"]
        querystring = {
            "interval": candle_size,
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "datatype":"json",
            "output_size":"compact"}
        return await cls.call_api("alphavantage", url, headers, querystring)

    @classmethod
    async def call_alphavantage_api(cls, symbol, duration, candle_size):
        url = apis["alphavantage"]["url"]
        headers = apis["alphavantage"]["headers"]

        querystring = {
            "function":"TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize":"compact",
            "datatype":"json"}
        return await cls.call_api("alphavantage", url, headers, querystring)

    @classmethod
    async def call_apistocks_api(cls, symbol, duration, candle_size):
        dateEnd = datetime.datetime.now().date()
        duration_prefix, duration_suffix = break_string(duration)
        dateStart = dateEnd
        if duration_suffix == 'Y':
            dateStart -= relativedelta(years=1)
        else:
            dateStart -= relativedelta(months=int(duration_prefix))

        url = apis["apistocks"]["url"]
        headers = apis["apistocks"]["headers"]
        querystring = {
            "symbol": symbol,
            "dateStart": dateStart.strftime("YYYY-MM-DD"),
            "dateEnd": dateEnd.strftime("YYYY-MM-DD")}
        return await cls.call_api("apistocks", url, headers, querystring)

    @classmethod
    async def api_data(cls, symbol, duration, candle_size):
        # if candle_size in ['1min', '5min', '15min', '30min', '60min']:
        #     return await cls.call_alphavantage_intraday_api(symbol, candle_size)
        # response = await cls.auto_select_api(symbol, duration, candle_size)
        response = await cls.call_alphavantage_api(symbol, duration, candle_size)
        return response

    @classmethod
    async def format_data(cls, res):
        pass

if __name__ == '__main__':
    response = asyncio.run(StockDataApi.api_data('IBM', '1M', '1D'))
