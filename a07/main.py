#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 09:08
# Author:  rongli
# Email:   abc@xyz.com
# File:    hello.py
# Project: fastapi_course
# IDE:     PyCharm
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

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
    return {"Hello": "World"}


media_dir = Path(__file__).absolute().parent


class FolderMaker:
    def __init__(self, upload_to: str):
        self.upload_to = upload_to
        self.dir_path = None

    def __call__(self, req: Request):
        dir_path = media_dir / self.upload_to
        # 检查目录存不存在等等
        self.dir_path = str(dir_path)
        return self

    def upload_to_qiniu(self):
        print("我是要上传到七牛的")


@app.get("/upload/image", summary="类做为依赖 - 上传图片")
def auth_admin(folder_maker: FolderMaker = Depends(FolderMaker("image"))):
    print(folder_maker.dir_path)
    folder_maker.upload_to_qiniu()
    return {"msg": "ok"}


@app.get("/upload/pdf", summary="类做为依赖 - 上传pdf")
def auth_admin(dir_name: FolderMaker = Depends(FolderMaker("pdf"))):
    return {"msg": dir_name}
