#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-07-27 21:07
# Author:  rongli
# Email:   abc@xyz.com
# File:    conf.py
# Project: fa-demo
# IDE:     PyCharm
from pathlib import Path

from pydantic import BaseSettings


# 文档：https://pydantic-docs.helpmanual.io/usage/settings/

class Settings(BaseSettings):
    class Config:
        # 环境变量文件
        env_file = ".env"

    # debug模式
    debug: bool = True

    # jwt加密的 key
    jwt_secret_key: str = "abcdefghijklmn"
    # jwt加密算法
    jwt_algorithm: str = 'HS256'
    # token过期时间，单位：秒
    jwt_exp_seconds: int = 60 * 60

    # 项目标题
    project_title = 'FastAPI 后端'
    # 项目描述
    project_description = '一个牛逼的API后端'
    # 项目版本
    project_version = '0.0.1'

    # url的前缀
    url_prefix: str = "/api/v1"
    # host
    server_host: str = 'localhost'
    server_port: int = 8000

    #  swagger docs 的登陆重定向地址
    swagger_ui_oauth2_redirect_url: str = url_prefix + '/test/token'

    # 项目根目录
    base_dir = Path(__file__).absolute().parent.parent.parent
    # 日志目录
    log_dir = base_dir / 'logs'
    # 静态资源
    static_dir = base_dir / 'static'
    static_url_prefix: str = '/static'
    # 用户上传目录
    media_dir = base_dir / 'media'
    media_url_prefix: str = '/media'
