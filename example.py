import asyncio
import aiohttp
from DetaCache import detaCache
from deta import Deta

db = Deta('project_key').Base("base_name")


@detaCache(dbCache=db,urlArg='url')
async def getjSON(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not response.status == 404:
                return await response.json()
            return None

async def main():
    data = await getjSON(url='https://httpbin.org/json')
    print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

