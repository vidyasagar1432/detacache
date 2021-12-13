import asyncio
import aiohttp
import requests

from funcy.debug import print_durations
from detacache import DetaCache,Aiohttp,Requests



# cache = DetaCache('c0reypnf_MSMvWY1BqNaDFgAvsPe9YJ9nqPiKNt9Z')

# api = Aiohttp('c0reypnf_MSMvWY1BqNaDFgAvsPe9YJ9nqPiKNt9Z')
api = Requests('c0reypnf_MSMvWY1BqNaDFgAvsPe9YJ9nqPiKNt9Z')

# @deta.cache(log=True,expire=15)
# async def detaAsyncgetjSON(url:str):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.json()


# @deta.cache(log=True,expire=15)
# def detaSyncgetjSON(url:str):
#     return requests.get(url).json()


# async def getjSON(url:str):
#     return await api.getJson(url,ttl=20,log=True)

def getjSON(url:str):
    return api.getJson(url,ttl=20,log=True)


async def main():
    with print_durations('RAW'):
        data =getjSON('https://httpbin.org/json')
    # with print_durations('deta cached'):
    #     data = await detaAsyncgetjSON('https://httpbin.org/user-agent')
    #     print(data)
    #     print(detaSyncgetjSON('https://httpbin.org/user-agent'))
        print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())