#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 12:54
# Author:  rongli
# Email:   abc@xyz.com
# File:    profile.py
# Project: fastapi_course
# IDE:     PyCharm


from fastapi import APIRouter, Path

router = APIRouter(prefix='/profile', tags=['资料管理'])


@router.get("", summary="查看所有资料")
def get_profile_list():
    return 'get_profile_list'


@router.get("/{pid}", summary="查看指定 profile")
def get_one_profile(pid: int = Path(...)):
    return f'get_one_profile: {pid}'
