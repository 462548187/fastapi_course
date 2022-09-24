#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:29
# Author:  rongli
# Email:   abc@xyz.com
# File:    dev.py
# Project: notebook
# IDE:     PyCharm
import datetime

from fastapi import APIRouter

router = APIRouter(prefix='/dev', tags=['开发调试用接口'])


@router.get('/ping', summary='ping')
def ping():
    return {"msg": "pong"}


@router.get('/now', summary='ping')
def now():
    return {"now": datetime.datetime.now()}
