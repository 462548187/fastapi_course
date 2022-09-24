#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:34
# Author:  rongli
# Email:   abc@xyz.com
# File:    __init__.py.py
# Project: notebook
# IDE:     PyCharm


from fastapi import APIRouter

from .home import router as home_router

views_router = APIRouter(tags=['视图路由'])

views_router.include_router(home_router)
