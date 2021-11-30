# [DetaCache](https://github.com/vidyasagar1432/DetaCache)

#### Async Function Decorator to cache to Deta base.

## Installing

```bash
pip3 install DetaCache
```

## Async
```python
import asyncio
import aiohttp
from DetaCache import detaCache
from deta import Deta

db = Deta('project_key').Base("base_name")


@detaCache(dbCache=db,urlArg='url')
async def getjSON(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    data = await getjSON(url='https://httpbin.org/json')
    print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## License

MIT License

Copyright (c) 2021 [Vidya Sagar](https://github.com/vidyasagar1432)