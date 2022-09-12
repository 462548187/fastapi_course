#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 09:08
# Author:  rongli
# Email:   abc@xyz.com
# File:    hello.py
# Project: fastapi_course
# IDE:     PyCharm

from fastapi import Body, FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles

from a09.docs import custom_docs

app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/static', StaticFiles(directory='static'))

custom_docs(app)


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
# if request.headers['host']=="localhost:8000":
#     request.state.user="admin"
# print(request.url)

# scope receive send
# data = await request.body()
# print("----->",data)
# async def request_body():
#     return {'type': 'http.request', 'body': data, 'more_body': False}
#
# request = Request(request.scope, request_body)
# 在 call_next 之前
# if request.url.path == "/":
#     return JSONResponse({"msg": "bye~"}, status_code=400)
# response = await call_next(request)
# process_time = time.time() - start_time
# response.headers["X-Process-Time"] = f"{process_time * 1000:.3f}ms"

# 拿到响应体的 body
# body_data = []
#
# async def response_body():
#     for data in body_data:
#         yield data
#     yield b""
#
# async for chunk in response.body_iterator:
#     if not isinstance(chunk, bytes):
#         chunk = chunk.encode(response.charset)
#     body_data.append(chunk)
#     print("---->", f"{chunk=}")
# response = StreamingResponse(status_code=response.status_code,
#                              content=response_body(),
#                              headers=dict(response.headers))
# return response

class MiddlewareTest:
    def __init__(self, name: str):
        self.name = name

    async def test_order(self, request: Request, call_next):
        print(f"{self.name} start ")
        response = await call_next(request)
        print(f"{self.name} end ")
        return response

    def __call__(self, app: FastAPI):
        app.middleware("http")(self.test_order)


MiddlewareTest("  m1")(app)
MiddlewareTest("m2")(app)


@app.post("/hi")
def home(data: dict = Body(...), q: str = Query(...)):
    return {"Hello": data, "query": q}


@app.get("/")
def home(req: Request):
    print("   hello")
    # print("------>", req.state.user)
    return {"Hello": "world"}
