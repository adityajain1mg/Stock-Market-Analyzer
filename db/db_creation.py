from sanic.log import logger
from tortoise import Tortoise
from config import TORTOISE_ORM

class CreateDB:
    @classmethod
    async def init(cls):
        logger.info("scheme generated")
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        cls._db = Tortoise.get_connection("default")
        

    @classmethod
    async def run_query(cls):
        query = """select api
                    from apiresponse 
                    where  EXTRACT(EPOCH FROM (current_timestamp - hit_time)) < 30
                    group by api
                    order by avg(successful_hits) desc
                    limit 1"""
        
        con = await cls._db.execute_query_dict(query)
        return con

    @classmethod
    async def close(cls):
        cls._db.close()