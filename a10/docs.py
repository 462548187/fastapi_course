#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-11 17:19
# Author:  rongli
# Email:   abc@xyz.com
# File:    docs.py
# Project: fastapi_course
# IDE:     PyCharm
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html


async def custom_swagger_ui_html(req: Request):
    return get_swagger_ui_html(
            openapi_url=req.app.openapi_url,
            title=req.app.title + " - Swagger UI",
            oauth2_redirect_url=req.app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger/swagger-ui.css")


async def custom_redoc_html(req: Request):
    return get_redoc_html(
            openapi_url=req.app.openapi_url,
            title=req.app.title + " - ReDoc",
            redoc_js_url="/static/redoc/redoc.standalone.js")


def custom_docs(app: FastAPI):
    app.get("/docs", include_in_schema=False)(custom_swagger_ui_html)
    app.get("/docs", include_in_schema=False)(custom_redoc_html)
