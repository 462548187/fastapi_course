#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-03 20:35
# Author:  rongli
# Email:   abc@xyz.com
# File:    models.py
# Project: fastapi_course
# IDE:     PyCharm
from pydantic import BaseModel, Field, validator


class UserInDB(BaseModel):
    """ 这个模型是orm模型 """
    username: str
    password: str
    is_superuser: bool = False
    status: bool = True


class UserSignUp(BaseModel):
    username: str = Field(..., example="tom")
    password: str = Field(..., example="123")
    password2: str = Field(..., example="123")

    @validator("password2")
    def two_password_match(cls, value, values):
        if value != values['password']:
            raise ValueError("两个密码必须一致")
        return value


class UserLogin(BaseModel):
    username: str= Field(..., example="tom")
    password: str= Field(..., example="123")


class UserInfo(BaseModel):
    username: str
    is_superuser: bool = False
    status: bool = True