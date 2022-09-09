#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:07
# Author:  rongli
# Email:   abc@xyz.com
# File:    conf.py
# Project: fa-demo
# IDE:     PyCharm

from pydantic import BaseSettings


# 文档：https://pydantic-docs.helpmanual.io/usage/settings/

class Settings(BaseSettings):
    # debug模式
    debug: bool = True

    # jwt加密的 key
    jwt_secret_key: str = "abcdefghijklmn"
    # jwt加密算法
    jwt_algorithm: str = 'HS256'
    # token过期时间，单位：秒
    jwt_exp_seconds: int = 60 * 60


settings = Settings()
