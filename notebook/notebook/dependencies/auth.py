#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-03 22:10
# Author:  rongli
# Email:   abc@xyz.com
# File:    auth.py
# Project: fastapi_course
# IDE:     PyCharm
from datetime import datetime, timedelta
from logging import getLogger

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError

from ..config import settings
from ..libs.db_lib import db

logger = getLogger(__name__)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.swagger_ui_token_url)

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl=settings.oauth_authorization_url,
                                              tokenUrl=settings.oauth_token_url,
                                              scopes={"read": "读取用户信息"}
                                              )


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
        logger.exception("token解码失败")
        raise HTTPException(status_code=401, detail="token已失效，请重新登陆！")
    # 2. 根据 payload 中的信息去数据库中找到对应的用户
    username = payload.get("username")
    user = db.get_or_none(username)
    if user is None:
        raise HTTPException(status_code=401, detail="认证不通过")
    return user
