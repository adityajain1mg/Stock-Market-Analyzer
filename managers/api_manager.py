import asyncio
import requests
import re
from sanic.exceptions import BadRequest, NotFound
from common import api_list, apis, api_stats
from utils import  break_string
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

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
            res = requests.get(url, headers=headers, params=querystring, timeout=5)
            api_stats[api]["success"] += 1
            response = res.json()
            if len(response.keys()) == 1:
                raise BadRequest(response)
            return response
        except Exception as e:
            api_stats[api]["failure"] += 1
            raise BadRequest(e)

    @classmethod
    async def call_alphavantage_intraday_api(cls, symbol, duration, candle_size):
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
        res = await cls.call_api("alphavantage", url, headers, querystring)
        return await cls.format_alphavantage_data(res, duration)

    @classmethod
    async def call_alphavantage_api(cls, symbol, duration, candle_size):
        url = apis["alphavantage"]["url"]
        headers = apis["alphavantage"]["headers"]

        querystring = {
            "function":"TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize":"compact",
            "datatype":"json"}
        res = await cls.call_api("alphavantage", url, headers, querystring)
        return await cls.format_alphavantage_data(res, duration)

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
            "dateStart": dateStart,
            "dateEnd": dateEnd}
        res = await cls.call_api("apistocks", url, headers, querystring)
        return await cls.format_apistocks_data(res)
        

    @classmethod
    async def api_data(cls, symbol, duration, candle_size):
        if candle_size in ['1min', '5min', '15min', '30min', '60min']:
            return await cls.call_alphavantage_intraday_api(symbol, duration, candle_size)
        response = await cls.auto_select_api(symbol, duration, candle_size)
        return response
        # return await cls.call_apistocks_api(symbol, duration, candle_size)

    @classmethod
    async def format_alphavantage_data(cls, data, duration):
        second_key = list(data.keys())[1]
        second_value = data[second_key]
        second_value = pd.DataFrame(second_value).T
        second_value['Date'] = second_value.index
        second_value
        second_value['4. close'] = second_value['4. close'].astype(float)
        df = second_value[['Date', '4. close']]
        df = df[::-1]

        today_date = datetime.datetime.now().date()
        duration_prefix, duration_suffix = break_string(duration)
        final_date = today_date
        if duration_suffix == 'Y':
            final_date -= relativedelta(years=1)
        else:
            final_date -= relativedelta(months=int(duration_prefix))
        
        start_date = final_date.strftime('%Y-%m-%d')
        end_date = today_date.strftime('%Y-%m-%d')
        df = df.loc[(df.index >= start_date) & (df.index <= end_date)]
        
        return df

    @classmethod
    async def format_apistocks_data(cls, data):
        second_key = list(data.keys())[1]
        second_value = data[second_key]
        second_value = pd.DataFrame(second_value)
        df = second_value[['Date', 'Close']]
        df.rename(columns={'Close': '4. close'}, inplace=True)
        return df

if __name__ == '__main__':
    response = asyncio.run(StockDataApi.api_data('IBM', '1M', '1D'))
    print(response)