#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 09:08
# Author:  rongli
# Email:   abc@xyz.com
# File:    hello.py
# Project: fastapi_course
# IDE:     PyCharm
from typing import List

from fastapi import Body, Cookie, FastAPI, Header, Path, Query
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi import Request


app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/static', StaticFiles(directory='static'))


# <editor-fold desc="解决 docs 文档加载慢的问题">
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger/swagger-ui.css")


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc/redoc.standalone.js")


# </editor-fold>


@app.get("/")
def home():
    return {"Hello": "World - a03"}


@app.get("/path/{p}", summary="路径参数")
def get_path(p: str = Path(...)):
    return {"msg": p}


@app.get("/path/class/{c_id}/student/{s_id}", summary="多个路径参数")
def get_multi_path(c_id: int = Path(...), s_id: int = Path(...)):
    return {"c_id": c_id, "s_id": s_id}


@app.get("/query", summary="查询参数")
def get_query(p: str = Query(...)):
    return {"msg": p}


@app.get("/query/page", summary="分页查询")
def get_query_page(page: int = Query(1, gt=0, description="当前页码"),
                   page_size: int = Query(10, gt=0, le=100, description="每页数量", alias="pageSize")):
    return {"page": page, "page_size": page_size}


@app.get("/query/order", summary="按多个字段排序")
def get_query_order(p: List[str] = Query(..., description="按指定的字段排序，可指定多个")):
    return {"msg": p}


@app.post("/body/base", summary="body - 基本使用")
def post_body(p: str = Body(..., title='car')):
    return {"msg": p}


class Car(BaseModel):
    name: str = Field(..., description="名称")
    brand: str = Field(..., max_length=10)
    price: float = Field(..., gt=0, example=10, description="价格(万)")


@app.post("/body/dict", summary="body - 传一个字典")
def post_body_dict(p: Car = Body(...)):
    return {"msg": p}


@app.post("/body/list", summary="body - 同时传多个字典")
def post_body_list(p: List[Car] = Body(...)):
    return {"msg": p}


@app.post("/header", summary="获取 Header 参数")
async def get_header_param(param: str = Header(..., description="自定义 Header", alias="Authorization")):
    """
    ## 当使用 `Authorization` 或 `authorization` 时，docs界面不会自动发送请求头
    ## 请使用 `Apipost` 或者 `postman` 测试这个接口
    ## 关于参数名自动转换的问题，请查看官方文档 [传送门](https://fastapi.tiangolo.com/zh/tutorial/header-params/#_1)
    """
    return {"param": param}


@app.get("/cookie", summary="获取 Cookie 参数")
async def get_cookie_param(param: str = Cookie(None, alias="CocaCola", description="自定义 Cookie", example="PepsiCo")):
    """
    ## 请使用 `Apipost` 或者 `postman` 测试这个接口，在 header 中设置 `cookie` 注意是小写的 `c`
    """
    return {"param": param}


@app.get("/echo", summary="request 对象")
async def get_request(req: Request):
    print(req)
    return {
        "base_url": req.base_url,
        "client": req.client,
        "cookies": req.cookies,
        "headers": req.headers,
        "method": req.method,
        "path_params": req.path_params,
        "query_params": req.query_params,
        "scope": {k: str(v) for k, v in req.scope.items()},
        "url": req.url,
        }
