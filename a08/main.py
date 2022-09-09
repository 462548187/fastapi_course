#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 09:08
# Author:  rongli
# Email:   abc@xyz.com
# File:    hello.py
# Project: fastapi_course
# IDE:     PyCharm

from fastapi import Body, Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles

from a08.auth import auth_depend, create_access_token
from a08.config import settings
from a08.libs.db_lib import db
from a08.libs.hash_lib import hash_tool
from a08.models import UserInDB, UserInfo, UserSignUp

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
def home():
    return {"Hello": "World - a08"}


@app.post("/signup", summary="注册接口")
def signup(form_data: UserSignUp = Body(...)):
    # 拿到前端传过来的数据
    username = form_data.username
    password = form_data.password
    # 校验数据
    pass
    # 根据用户名去数据库里面查对应的 user
    user = db.get_or_none(username)
    # 如果已经有了，就返回错误信息
    if user is not None:
        return {"msg": "当前用户名已经被占用了"}
    # 保存到数据库
    encode_pwd = hash_tool.encrypt_password(password)
    user = UserInDB(username=username, password=encode_pwd)
    db.save(user)
    # 给前端响应信息
    return {'msg': "ok"}


@app.post("/login", summary="登陆接口")
def login():
    return {"msg": "login"}


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
    app.post("/token", summary="获取 token 接口")(get_token)

@app.get("/me", summary="个人信息")
def get_my_info(me: UserInDB = Depends(auth_depend)):
    user_info = UserInfo(**me.dict())
    return {"msg": user_info}


@app.get("/vip", summary="查看 VIP 信息", dependencies=[Depends(auth_depend)])
def get_vip_info():
    return {"msg": "vip info"}
