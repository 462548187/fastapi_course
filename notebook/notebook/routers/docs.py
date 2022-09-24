#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:07
# Author:  rongli
# Email:   abc@xyz.com
# File:    docs.py
# Project: notebook
# IDE:     PyCharm
from fastapi import APIRouter, Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.security import OAuth2PasswordRequestForm

from ..config import settings
from ..dependencies import create_access_token
from ..libs.db_lib import db
from ..utils import hash_tool

router = APIRouter()


def custom_docs(application: FastAPI):
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
                openapi_url=application.openapi_url,
                title=application.title + " - Swagger UI",
                oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
                swagger_js_url="/static/swagger/swagger-ui-bundle.js",
                swagger_css_url="/static/swagger/swagger-ui.css")

    async def redoc_html():
        return get_redoc_html(
                openapi_url=application.openapi_url,
                title=application.title + " - ReDoc",
                redoc_js_url="/static/redoc/redoc.standalone.js")

    def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
        # 第一步 拿到 用户名 和密码 ，校验
        username = form_data.username
        password = form_data.password
        # 第二步 通过用户名去数据库中查找到对应的 user
        user = db.get_or_none(username)
        if user is None:
            return {"msg": "登陆失败，用户名与密码不匹配"}
        # 第三步 检查密码
        if not hash_tool.check_password(user.password, password):
            return {"msg": "登陆失败，用户名与密码不匹配"}
        # 第四步 生成 token
        # Authorization: bearer header.payload.sign
        token = create_access_token({"username": username})
        # 给前端响应信息
        # return {"token": f"bearer {token}"}
        return {"access_token": token, "token_type": "bearer"}

    if settings.debug:
        application.get("/docs", include_in_schema=False)(custom_swagger_ui_html)
        application.get("/redoc", include_in_schema=False)(redoc_html)
        application.post(settings.swagger_ui_oauth2_redirect_url,
                         summary="获取 token 接口",
                         tags=['获取 token 接口'])(get_token)
