import asyncio
import aiohttp
import requests

from detacache import DetaCache


app = DetaCache(projectKey='projectKey')


@app.cache(expire=20)
async def asyncgetJson(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


@app.cache(expire=20)
async def asyncgetText(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


@app.cache(expire=10)
def syncgetJson(url: str):
    return requests.get(url).json()


@app.cache(expire=10)
def syncgetText(url: str):
    return requests.get(url).text


async def main():
    asyncJsonData = await asyncgetJson('https://httpbin.org/json')
    print(asyncJsonData)
    syncJsonData = syncgetJson('https://httpbin.org/json')
    print(syncJsonData)
    asyncTextData = await asyncgetText('https://httpbin.org/html')
    print(asyncTextData)
    syncTextData = syncgetText('https://httpbin.org/html')
    print(syncTextData)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
