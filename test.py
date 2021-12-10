import asyncio
import aiohttp
import requests

from funcy.debug import print_durations
from DetaCache import detaCache, localCache
# from DetaCache import localCache

local = localCache('cache.json')

deta = detaCache('c0reypnf_MSMvWY1BqNaDFgAvsPe9YJ9nqPiKNt9Z')

@local.cacheAsyncFunction(expire=15,log=True)
async def localAsyncgetjSON(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


@local.cacheSyncFunction(expire=15,log=True)
def localSyncgetjSON(url:str):
    return requests.get(url).json()


@deta.cacheAsyncFunction(expire=15,log=True)
async def detaAsyncgetjSON(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


@deta.cacheSyncFunction(expire=15,log=True)
def detaSyncgetjSON(url:str):
    return requests.get(url).json()


# def getjSON(url:str):
#     return requests.get(url).json()


async def main():
    # with print_durations('RAW'):
    #     getjSON('https://httpbin.org/json')
    with print_durations('deta cached'):
        await detaAsyncgetjSON('https://httpbin.org/json')
        detaSyncgetjSON('https://httpbin.org/json')
    with print_durations('local cached'):
        print(localSyncgetjSON('https://api-ipify.vercel.app/ip'))
        data = await localAsyncgetjSON('https://httpbin.org/json')
        print(data)
        print(localSyncgetjSON('https://httpbin.org/json'))
        
        


loop = asyncio.get_event_loop()
loop.run_until_complete(main())