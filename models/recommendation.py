from datetime import datetime, timedelta
from models.db import ApiResponse
import pandas as pd

class Recommendation:

    @classmethod
    async def find_recent_requests(cls):

        thirty_seconds_ago = datetime.utcnow() - timedelta(seconds=30)
        requests = await ApiResponse.filter(
            timestamp__gte=thirty_seconds_ago
        ).values('api', 'successful_hits')
        return requests

    @classmethod
    async def highest_success_api(cls):
        result = await cls.find_recent_requests()
        api_total_attempts = {'alphavantage': 0, 'apistocks': 0}
        api_successful_attempts = {'alphavantage': 0, 'apistocks': 0}


        for row in result:
            api = row['api']
            success = row['successful_hits']
            if api in api_total_attempts:
                api_total_attempts[api] += 1
                if success == 1:
                    api_successful_attempts[api] += 1

        api_success_rates = {
            'alphavantage': api_successful_attempts['alphavantage'] / api_total_attempts['alphavantage'] if api_total_attempts[
                                                                                              'alphavantage'] != 0 else 0,
            'apistocks': api_successful_attempts['apistocks'] / api_total_attempts['apistocks'] if api_total_attempts[
                                                                                           'apistocks'] != 0 else 0
        }

        highest_success_rate_api = "alphavantage"
        max_success = api_success_rates['alphavantage']

        for key, value in api_success_rates.items():
            if value > max_success:
                max_success = value
                highest_success_rate_api = key

        response = {'api': "{}".format(highest_success_rate_api.lower())}
        return response