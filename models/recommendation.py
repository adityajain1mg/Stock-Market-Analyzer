from datetime import datetime, timedelta
from models.db import ApiResponse
import pandas as pd
from db.db_creation import CreateDB
from sanic.log import logger

class Recommendation:

    @classmethod
    async def find_recent_requests(cls):

        thirty_seconds_ago = datetime.utcnow() - timedelta(seconds=30)
        requests = await ApiResponse.filter(
            hit_time__gte=thirty_seconds_ago
        ).values('api', 'successful_hits')
        res = await ApiResponse.filter()
        return requests

    @classmethod
    async def highest_success_api(cls):
        query_result = await CreateDB.run_query()

        max_success_rate_api = "alphavantage"
        if len(query_result) != 0: 
            max_success_rate_api = query_result[0]['api']
        logger.info(max_success_rate_api)

        response = {'api': "{}".format(max_success_rate_api.lower())}
        return response