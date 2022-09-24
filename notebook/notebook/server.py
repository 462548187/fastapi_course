#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 09:08
# Author:  rongli
# Email:   abc@xyz.com
# File:    hello.py
# Project: fastapi_course
# IDE:     PyCharm

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .routers import api_router, custom_docs
from .views import views_router

# 实例化 fastapi 对象
app = FastAPI(docs_url=None, redoc_url=None,
              title=settings.project_title,
              description=settings.project_description,
              version=settings.project_version)

# 自定义 docs 界面
custom_docs(app)

# 挂载 api 路由
app.include_router(api_router)
# 挂载 view 路由
app.include_router(views_router)

# 挂载静态文件目录
app.mount(settings.static_url_prefix, StaticFiles(directory=settings.static_dir))
# 用户上传的文件
app.mount(settings.media_url_prefix, StaticFiles(directory=settings.media_dir))
