#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-03 22:10
# Author:  rongli
# Email:   abc@xyz.com
# File:    auth.py
# Project: fastapi_course
# IDE:     PyCharm
import traceback
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from a08.config import settings
from a08.libs.db_lib import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_exp_seconds)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def auth_depend(token: str = Depends(oauth2_scheme)):
    # 1. 解析 token 中的 payload 信息
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        exc_msg = '\n' + "-" * 40 + "  catch some exceptions  " + "-" * 40 + '\n'
        exc_msg += traceback.format_exc() + '\n'
        local_vars = locals()
        del local_vars['exc_msg']
        exc_msg += f"{local_vars=}" + '\n'
        exc_msg += "-" * 100
        print(exc_msg)
        raise HTTPException(status_code=401, detail="token已失效，请重新登陆！")
    # 2. 根据 payload 中的信息去数据库中找到对应的用户
    username = payload.get("username")
    user = db.get_or_none(username)
    if user is None:
        raise HTTPException(status_code=401, detail="认证不通过")
    return user
