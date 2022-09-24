#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:07
# Author:  rongli
# Email:   abc@xyz.com
# File:    __init__.py.py
# Project: notebook
# IDE:     PyCharm
from fastapi import APIRouter

from .dev import router as dev_router
from .docs import custom_docs
from .user import router as user_router
from ..config import settings

api_router = APIRouter(prefix=settings.url_prefix)

if settings.debug:
    api_router.include_router(dev_router)

api_router.include_router(user_router)
