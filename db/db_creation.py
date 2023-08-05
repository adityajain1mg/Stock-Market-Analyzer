from sanic.log import logger
from tortoise import Tortoise
from config import TORTOISE_ORM

class CreateDB:
    @classmethod
    async def init(cls):
        logger.info("scheme generated")
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()

            
    