from src.service.config import SQLConfig
import uvloop
from asyncpg import connect, create_pool


class AsyncDB:
    uri = SQLConfig.SQLALCHEMY_DATABASE_URI

    def execute(self, execute_sql=None):
        _loop = uvloop.new_event_loop()
        _result = _loop.run_until_complete(async_execute(self.uri, execute_sql))
        _loop.close()

        return _result


async def async_execute(uri, _count_sql):
    try:
        print('connection - create_pool - async')
        _pool = await create_pool(uri, max_size=50)
        async with _pool.acquire() as connection:
            _results = await connection.fetch(_count_sql)

            return _results

    except Exception as ex:
        print(str(ex)[0:500])
        return None


async_conn = AsyncDB()
