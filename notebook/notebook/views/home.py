#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:34
# Author:  rongli
# Email:   abc@xyz.com
# File:    home.py
# Project: notebook
# IDE:     PyCharm

from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from ..dependencies import create_access_token
from ..extends import fast_oauth

router = APIRouter()


# 如果需要在 /docs 页面使用这种 oauth 认证方式，
# 应该使用 OAuth2AuthorizationCodeBearer 代替原来的 OAuth2PasswordBearer
# /docs页面，访问顺序 auth_url -> callback -> token_url

@router.get('/', summary='首页', response_class=HTMLResponse)
async def home(request: Request):
    context = {'request': request, 'auth_url': fast_oauth.auth_url}
    return request.app.state.jinja.TemplateResponse("index.html", context=context)


# @router.get('/callback')
# @router.get('/docs/oauth2-redirect')
async def callback(code: str = Query(...), state: str = Query(...)):
    # 用code获取 token
    print(code, state)

    token = fast_oauth.get_token(code, state)
    # 用token 获取用户信息
    user_info = fast_oauth.get_user_info(token)
    # 记录用户信息
    # 这里面应该用 user_info 里面的 id 或者用户名去查一下，
    # 如果是第一次注册过来的，应该引导用户去完善个人信息，
    # 如果是已经登陆过的用户，应该给跳到首页或者来的页面
    print(user_info)
    # 创建token并返回
    # return HTMLResponse("<h1>登陆成功了</h1>")

    token = create_access_token({"username": "tom"})
    # 给前端响应信息
    # return {"token": f"bearer {token}"}
    return {"access_token": token, "token_type": "bearer"}
