#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 12:51
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py.py
# Project: fastapi_course
# IDE:     PyCharm

from fastapi import APIRouter, Path

router = APIRouter(prefix='/user', tags=['用户管理'])


# /user
@router.get("", summary="查看用户列表")
def get_user_list():
    return 'user_list'


# /user/2
@router.get("/{uid}", summary="查看指定用户")
def get_one_user(uid: int = Path(...)):
    return f'get_one_user: {uid}'
