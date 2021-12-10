import asyncio
import aiohttp
import requests

from funcy.debug import print_durations
from DetaCache import detaCache


deta = detaCache('projectKey')


@deta.cacheAsyncFunction(expire=10)
async def detaAsyncgetjSON(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


@deta.cacheSyncFunction()
def detaSyncgetjSON(url:str):
    return requests.get(url).json()


def getjSON(url:str):
    return requests.get(url).json()


async def main():
    with print_durations('RAW'):
        getjSON('https://httpbin.org/json')
    with print_durations('deta cached'):
        await detaAsyncgetjSON('https://httpbin.org/json')
        detaSyncgetjSON('https://httpbin.org/json')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())