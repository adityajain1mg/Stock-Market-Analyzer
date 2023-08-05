import asyncio
import datetime
import pandas as pd
from aiohttp_client_cache import CachedSession, SQLiteBackend
from dateutil.relativedelta import relativedelta
from sanic.exceptions import BadRequest
from sanic.log import logger
from utils import break_string
from models.recommendation import Recommendation
from models.data import SaveResponse

import os
from dotenv import load_dotenv
load_dotenv()

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
                    
                    if response.status != 200 or len(res.keys()) == 1 or len(res[list(res.keys())[1]]) == 0 :
                        await SaveResponse.save_request(api, 0)
                        raise BadRequest(res)
                        
                    await SaveResponse.save_request(api, 1)
                    return res[list(res.keys())[1]]
        except TimeoutError:
            raise TimeoutError("Api call have exceeded the timeout limit")
       
    @classmethod
    async def _call_alphavantage_intraday_api(cls, symbol, duration, candle_size):
        """calling third party api to get intraday data
        """
        api_name = "alphavantage"
        url = os.getenv('aplhavantage_url')
        headers = {
                    "X-RapidAPI-Key": os.getenv('x_rapidapi_key'),
                    "X-RapidAPI-Host": os.getenv('alphavantage_host')
                }
        querystring = {
            "interval": candle_size,
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "datatype":"json",
            "output_size":"full"}
        res = await cls._call_api("alphavantage", url, headers, querystring)
        return await cls._format_alphavantage_data(res, duration)

    @classmethod
    async def _call_alphavantage_api(cls, symbol, duration, candle_size):
        """Calling third party api to get data"""
        url = os.getenv('aplhavantage_url')
        headers = {
                    "X-RapidAPI-Key": os.getenv('x_rapidapi_key'),
                    "X-RapidAPI-Host": os.getenv('alphavantage_host')
                }
        querystring = {
            "function":"TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize":"full",
            "datatype":"json"}
        res = await cls._call_api("alphavantage", url, headers, querystring)
        return await cls._format_alphavantage_data(res, duration)

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

        url = os.getenv('apistocks_url')
        headers = {
                    "X-RapidAPI-Key": os.getenv('x_rapidapi_key'),
                    "X-RapidAPI-Host": os.getenv('apistocks_host')
                }
        querystring = {
            "symbol": symbol,
            "dateStart": dateStart.strftime("%Y-%m-%d"),
            "dateEnd": dateEnd.strftime("%Y-%m-%d")}
        logger.info(querystring)
        res = await cls._call_api("apistocks", url, headers, querystring)
        return await cls._format_apistocks_data(res)
        
    @classmethod
    async def _auto_select_api(cls, symbol, duration, candle_size):
        """calling all the apis to get success rate of every api and then selecting
        maximum success rate api to get data
        """
        r = await Recommendation.highest_success_api()
        logger.info(r)
        max_rate_api = r.get('api')
        method = f'_call_{max_rate_api}_api'
        method_name = getattr(cls, method)
        data = await method_name(symbol, duration, candle_size)
        return data

    @classmethod
    async def api_data(cls, symbol, duration, candle_size):
        """Calling auto_select_api method to get data"""
        symbol = symbol.upper()
        if candle_size in ['1min', '5min', '15min', '30min', '60min']:
            return await cls._call_alphavantage_intraday_api(symbol, duration, candle_size)
        response = await cls._auto_select_api(symbol, duration, candle_size)
        return response

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