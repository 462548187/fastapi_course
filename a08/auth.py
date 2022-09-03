#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-03 22:10
# Author:  rongli
# Email:   abc@xyz.com
# File:    auth.py
# Project: fastapi_course
# IDE:     PyCharm
import traceback

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from a08.libs.db_lib import db
from a08.libs.jwt_lib import token_tool

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def auth_depend(token: str = Depends(oauth2_scheme)):
    # 1. 解析出 X-Auth 中的 token
    # bearer }\"mot\" :\"emanresu\"{
    # _, _, token = token.partition(" ")
    # 2. 解析 token 中的 payload 信息
    try:
        payload = token_tool.decode(token)
    except Exception as e:
        exc_msg = '\n' + "-" * 40 + "  catch some exceptions  " + "-" * 40 + '\n'
        exc_msg += traceback.format_exc() + '\n'
        local_vars = locals()
        del local_vars['exc_msg']
        exc_msg += f"{local_vars=}" + '\n'
        exc_msg += "-" * 100
        print(exc_msg)
        raise HTTPException(status_code=401, detail="认证不通过")
    # 3. 根据 payload 中的信息去数据库中找到对应的用户
    username = payload.get("username")
    user = db.get_or_none(username)
    if user is None:
        return {"msg": "认证不通过"}
    return user
