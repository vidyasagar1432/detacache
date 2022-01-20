
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,PlainTextResponse
from detacache import FastAPICache

import logging

logger = logging.getLogger("detacache")


app = FastAPI()

# templates = Jinja2Templates(directory='templates')

Cache = FastAPICache(projectKey='c0reypnf_MSMvWY1BqNaDFgAvsPe9YJ9nqPiKNt9Z')


# @app.get('/t-html')
# @Cache.cache(expire=10)
# def templateResponse(request:Request):
#     return templates.TemplateResponse('get.html',context={'request':request})

@app.get('/html')
@Cache.cache(expire=10)
def htmlResponse(request:Request):
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

@app.get('/json')
@Cache.cache(expire=10)
def json(request:Request):
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
@Cache.cache(expire=10)
def textResponse(request:Request):
    return PlainTextResponse('detacache')

@app.get('/str')
@Cache.cache(expire=10)
def strResponse(request:Request):
    return 'fastapi detacache'


@app.get('/tuple')
@Cache.cache(expire=10)
def tupleResponse(request:Request):
    return ('fastapi','detacache')

@app.get('/set')
@Cache.cache(expire=10)
def setResponse(request:Request):
    return {'fastapi','detacache'}


