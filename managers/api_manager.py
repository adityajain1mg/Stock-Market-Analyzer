import asyncio
import datetime
# import requests
import pandas as pd
from aiohttp_client_cache import CachedSession, SQLiteBackend
from dateutil.relativedelta import relativedelta
from sanic.exceptions import BadRequest, NotFound
from sanic.log import logger

from common import api_list, api_stats, apis
from utils import break_string

class StockDataApi:
    @classmethod
    async def _call_api(cls, api, url, headers, querystring):
        """calling third party apis and caching there response and raising exception
        """
        try:
            async with CachedSession(cache=SQLiteBackend('api_cache')) as session:
                async with session.get(url, headers=headers, params=querystring, ssl=False) as response:
                    if response.from_cache: 
                        logger.info("Cache is being used")
                    else:
                        logger.info("Data is saved in cache")

                    res = await response.json()
                    
                    if response.status != 200 and len(res.keys()) == 1:
                        raise BadRequest(res)
                    else: 
                        second_key = list(res.keys())[1]
                        second_value = res[second_key]
                        if len(second_value) == 0:
                            raise NotFound("Data is not available in the server")

                    api_stats[api]["success"] += 1

                    logger.info(api_stats)
                    return second_value
        except TimeoutError:
            raise TimeoutError("Api call have exceeded the timeout limit")
       

    @classmethod
    async def _call_alphavantage_intraday_api(cls, symbol, duration, candle_size):
        """calling third party api to get intraday data
        """
        api_name = "alphavantage"
        url = apis[api_name]["url"]
        headers = apis["alphavantage"]["headers"]
        querystring = {
            "interval": candle_size,
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "datatype":"json",
            "output_size":"full"}
        res = await cls.call_api("alphavantage", url, headers, querystring)
        return await cls.format_alphavantage_data(res, duration)

    @classmethod
    async def _call_alphavantage_api(cls, symbol, duration, candle_size):
        """Calling third party api to get data"""
        url = apis["alphavantage"]["url"]
        headers = apis["alphavantage"]["headers"]

        querystring = {
            "function":"TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize":"full",
            "datatype":"json"}
        res = await cls.call_api("alphavantage", url, headers, querystring)
        return await cls.format_alphavantage_data(res, duration)

    @classmethod
    async def _call_apistocks_api(cls, symbol, duration, candle_size):
        """Calling third party api to get data"""
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
            "dateStart": dateStart.strftime("%Y-%m-%d"),
            "dateEnd": dateEnd.strftime("%Y-%m-%d")}
        logger.info(querystring)
        res = await cls.call_api("apistocks", url, headers, querystring)
        return await cls.format_apistocks_data(res)
        
    @classmethod
    async def _auto_select_api(cls, symbol, duration, candle_size):
        """calling all the apis to get success rate of every api and then selecting
        maximum success rate api to get data
        """
        #add a time farme for success and failure and store in db
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
    async def api_data(cls, symbol, duration, candle_size):
        """Calling auto_select_api method to get data"""
        symbol = symbol.upper()
        if candle_size in ['1min', '5min', '15min', '30min', '60min']:
            return await cls.call_alphavantage_intraday_api(symbol, duration, candle_size)
        response = await cls.auto_select_api(symbol, duration, candle_size)
        return response
        # return await cls.call_apistocks_api(symbol, duration, candle_size)

    @classmethod
    async def _format_alphavantage_data(cls, second_value, duration):
        """formatting alphavantage api data"""
        second_value = pd.DataFrame(second_value).T
        second_value['Date'] = second_value.index
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
    async def _format_apistocks_data(cls, second_value):
        """Formatting apistocks data"""
        second_value = pd.DataFrame(second_value)
        df = second_value[['Date', 'Close']]
        df.rename(columns={'Close': '4. close'}, inplace=True)
        return df

if __name__ == '__main__':
    response = asyncio.run(StockDataApi.call_apistocks_api('IBM', '1M', '1D'))
    logger.info(response)