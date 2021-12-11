import asyncio
import aiohttp
import requests

from funcy.debug import print_durations
from detacache import DetaCache,CacheApi


deta = DetaCache('projectKey')


@deta.cache(log=True,expire=15)
async def detaAsyncgetjSON(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


@deta.cache(log=True,expire=15)
def detaSyncgetjSON(url:str):
    return requests.get(url).json()


def getjSON(url:str):
    return requests.get(url).json()


async def main():
    with print_durations('RAW'):
        getjSON('https://httpbin.org/json')
    with print_durations('deta cached'):
        data = await detaAsyncgetjSON('https://httpbin.org/user-agent')
        print(data)
        print(detaSyncgetjSON('https://httpbin.org/user-agent'))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())