from datetime import datetime
from sanic.log import logger
from models.db import ApiResponse


class SaveResponse:

    @classmethod
    async def save_request(cls, api, successful_hits):
        logger.info(api)
        timestamp = datetime.utcnow()
        request = ApiResponse(
            api = api,
            successful_hits=successful_hits,
            timestamp=timestamp
        )
        await request.save()
        logger.info("Successful")