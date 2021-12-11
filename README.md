# [DetaCache](https://github.com/vidyasagar1432/detacache)

#### Async and Sync Function Decorator to cache function call's to Deta base.

## Installing

```bash
pip3 install detacache
```

## Async and Sync Decorator to cache function
```python
import asyncio
import aiohttp
import requests

from DetaCache import detaCache

app = detaCache('projectKey')


@app.cache(expire=30)
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
```

## License

MIT License

Copyright (c) 2021 [Vidya Sagar](https://github.com/vidyasagar1432)