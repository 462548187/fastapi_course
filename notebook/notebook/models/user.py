#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:05
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py
# Project: notebook
# IDE:     PyCharm
from pydantic import BaseModel


class UserInDB(BaseModel):
    """ 这个模型是orm模型 """
    username: str
    password: str
    is_superuser: bool = False
    status: bool = True
