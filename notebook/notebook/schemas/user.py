#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:06
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py
# Project: notebook
# IDE:     PyCharm
from pydantic import BaseModel, Field, validator


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
    username: str = Field(..., example="tom")
    password: str = Field(..., example="123")


class UserInfo(BaseModel):
    username: str
    is_superuser: bool = False
    status: bool = True
