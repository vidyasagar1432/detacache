# [DetaCache](https://github.com/vidyasagar1432/detacache)

#### Async and Sync Function Decorator to cache function call's to Deta base.

## Installing

```bash
pip install detacache
```

## Async and Sync Decorator to cache function
```python
import asyncio
import aiohttp
import requests

from detacache import DetaCache

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

## FastAPI Decorator to cache function

#### you can use `cache` method as decorator between router decorator and view function and must pass `request` as param of view function.

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, PlainTextResponse
from detacache import FastAPICache

app = FastAPI()

templates = Jinja2Templates(directory='templates')

deta = FastAPICache(projectKey='projectKey')


@app.get('/t-html')
@deta.cache(expire=10)
def templateResponse(request:Request):
    return templates.TemplateResponse('home.html',context={'request':request})

@app.get('/html')
@deta.cache(expire=10)
def htmlResponse(request: Request):
    return HTMLResponse('''
        <!DOCTYPE HTML>
        <html lang="en-US">
        <head>
            <meta charset="UTF-8">
            <title>My Pimpin Website</title>
            <meta name="description" content="A sample website, nothin fancy">
            <meta http-equiv="author" content="Francisco Campos Arias">
            <meta name="keywords" content="html, css, web, design, sample, practice">
        </head>
        <body>
            <div class="container">
            <header>
                <div class="header">
                    <h1>{{ data }}</h1>
                </div>
            </header>
                <div class="main">
                    <h2>This is just an example with some web content. This is the Hero Unit.</h2>
                </div>
                <div class="feature">
                    <h3>Featured Content 1</h3>
                    <p>lorem ipsum dolor amet lorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum.</p>
                </div>
                <div class="feature">
                    <h3>Featured Content 2</h3>
                    <p>lorem ipsum dolor amet lorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor.</p>
                </div>
            <footer>
                &copy;2012 Francisco Campos Arias, All Rigts Reserved.
            </footer>
            </div>
        </body>
        </html>
        ''')


@app.get('/dict')
@deta.cache(expire=10)
def dictResponse(request: Request):
    return {
        "slideshow": {
            "author": "Yours Truly",
            "date": "date of publication",
            "slides": [
                {
                    "title": "Wake up to WonderWidgets!",
                    "type": "all"
                },
                {
                    "items": [
                        "Why <em>WonderWidgets</em> are great",
                        "Who <em>buys</em> WonderWidgets"
                    ],
                    "title": "Overview",
                    "type": "all"
                }
            ],
            "title": "Sample Slide Show"
        }
    }


@app.get('/text')
@deta.cache(expire=10)
def textResponse(request: Request):
    return PlainTextResponse('detacache')


@app.get('/str')
@deta.cache(expire=20)
async def strResponse(request: Request):
    return 'fastapi detacache'


@app.get('/tuple')
@deta.cache(expire=10)
def tupleResponse(request: Request):
    return ('fastapi', 'detacache')


@app.get('/list')
@deta.cache(expire=10)
def tupleResponse(request: Request):
    return ['fastapi', 'detacache']

@app.get('/set')
@deta.cache(expire=10)
def setResponse(request: Request):
    return {'fastapi', 'detacache'}


@app.get('/int')
@deta.cache(expire=10)
def intResponse(request: Request):
    return 10


@app.get('/float')
@deta.cache(expire=10)
def floatResponse(request: Request):
    return 1.5


@app.get('/bool')
@deta.cache(expire=10)
def boolResponse(request: Request):
    return True

```

## starlette Decorator to cache function

#### you can use `cache` method as decorator and must pass `request` as param of view function.

```python
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, PlainTextResponse, JSONResponse
from starlette.routing import Route
from starlette.requests import Request

from detacache import StarletteCache


deta = StarletteCache(projectKey='projectKey')



@deta.cache(expire=30)
def dictResponse(request: Request):
    return JSONResponse({
        "slideshow": {
            "author": "Yours Truly",
            "date": "date of publication",
            "slides": [
                {
                    "title": "Wake up to WonderWidgets!",
                    "type": "all"
                },
                {
                    "items": [
                        "Why <em>WonderWidgets</em> are great",
                        "Who <em>buys</em> WonderWidgets"
                    ],
                    "title": "Overview",
                    "type": "all"
                }
            ],
            "title": "Sample Slide Show"
        }
    })

@deta.cache(expire=20)
async def strResponse(request: Request):
    return JSONResponse('fastapi detacache') 

@deta.cache(expire=10)
def tupleResponse(request: Request):
    return JSONResponse(('fastapi', 'detacache'))

@deta.cache(expire=10)
def listResponse(req):
    print(req.url)
    return JSONResponse(['fastapi', 'detacache'])

@deta.cache(expire=10)
def setResponse(request: Request):
    return JSONResponse({'fastapi', 'detacache'})

@deta.cache(expire=10)
def intResponse(request: Request):
    return JSONResponse(10)

@deta.cache(expire=10)
def floatResponse(request: Request):
    return JSONResponse(1.5)

@deta.cache(expire=10)
def boolResponse(request: Request):
    return JSONResponse(True)

@deta.cache(expire=10)
def jsonResponse(request: Request):
    return JSONResponse({
        "slideshow": {
            "author": "Yours Truly",
            "date": "date of publication",
            "slides": [
                {
                    "title": "Wake up to WonderWidgets!",
                    "type": "all"
                },
                {
                    "items": [
                        "Why <em>WonderWidgets</em> are great",
                        "Who <em>buys</em> WonderWidgets"
                    ],
                    "title": "Overview",
                    "type": "all"
                }
            ],
            "title": "Sample Slide Show"
        }
    }
)

@deta.cache(expire=30)
def htmlResponse(request: Request):
    return HTMLResponse('''
        <!DOCTYPE HTML>
        <html lang="en-US">
        <head>
            <meta charset="UTF-8">
            <title>My Pimpin Website</title>
            <meta name="description" content="A sample website, nothin fancy">
            <meta http-equiv="author" content="Francisco Campos Arias">
            <meta name="keywords" content="html, css, web, design, sample, practice">
        </head>
        <body>
            <div class="container">
            <header>
                <div class="header">
                    <h1>{{ data }}</h1>
                </div>
            </header>
                <div class="main">
                    <h2>This is just an example with some web content. This is the Hero Unit.</h2>
                </div>
                <div class="feature">
                    <h3>Featured Content 1</h3>
                    <p>lorem ipsum dolor amet lorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum.</p>
                </div>
                <div class="feature">
                    <h3>Featured Content 2</h3>
                    <p>lorem ipsum dolor amet lorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor ametlorem ipsum dolor.</p>
                </div>
            <footer>
                &copy;2012 Francisco Campos Arias, All Rigts Reserved.
            </footer>
            </div>
        </body>
        </html>
        ''')

@deta.cache(expire=20)
def textResponse(request: Request):
    return PlainTextResponse('detacache')


routes = [
    Route("/text", endpoint=textResponse),
    Route("/html", endpoint=htmlResponse),
    Route("/json", endpoint=jsonResponse),
    Route("/bool", endpoint=boolResponse),
    Route("/float", endpoint=floatResponse),
    Route("/int", endpoint=intResponse),
    Route("/set", endpoint=setResponse),
    Route("/list", endpoint=listResponse),
    Route("/tuple", endpoint=tupleResponse),
    Route("/str", endpoint=strResponse),
    Route("/dict", endpoint=dictResponse),
]

app = Starlette(routes=routes)
```
## License

MIT License

Copyright (c) 2021 [Vidya Sagar](https://github.com/vidyasagar1432)