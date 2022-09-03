#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 09:08
# Author:  rongli
# Email:   abc@xyz.com
# File:    hello.py
# Project: fastapi_course
# IDE:     PyCharm
from typing import Dict, List

from fastapi import Depends, FastAPI, Query
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/static', StaticFiles(directory='static'))


# <editor-fold desc="docs">
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
def read_root():
    return {"Hello": "World - a05"}


def paginator(page: int = Query(1, gt=0, description="当前页码"),
              page_size: int = Query(10, gt=0, le=100, description="每页数量", alias="pageSize")) -> Dict[str, int]:
    return {"page": page, "page_size": page_size}


def order_by_filed(order_by: List[str] = Query(..., description="按给定的字段排序，可以输入多个字段")):
    return {"order": order_by}


def paginator_with_order(pg: Dict[str, int] = Depends(paginator), order: List[str] = Depends(order_by_filed)):
    return {"pg": pg, "order": order}


@app.get("/depends/page", summary="依赖的简单使用 - 分页")
def get_paginator(pg: Dict[str, int] = Depends(paginator)):
    return {"msg": pg}


@app.get("/depends/order", summary="依赖的简单使用 - 排序")
def get_order(order: List[str] = Depends(order_by_filed)):
    return {"msg": order}


@app.get("/depends/pg_plus", summary="依赖的嵌套 - 分页+排序")
def get_paginator_plus(pg_plus: dict = Depends(paginator_with_order)):
    return {"msg": pg_plus}
