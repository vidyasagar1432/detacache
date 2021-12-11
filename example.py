import asyncio
import aiohttp
import requests

from detacache import DetaCache


app = DetaCache(projectKey='projectKey')

@app.cache(expire=60)
async def asyncgetjSON(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

@app.cache(expire=30)
def syncgetjSON(url:str):
    return requests.get(url).json()

async def main():
    asyncdata = await asyncgetjSON('https://httpbin.org/json')
    print(asyncdata)
    syncdata = syncgetjSON('https://httpbin.org/json')
    print(syncdata)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

