#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:12
# Author:  rongli
# Email:   abc@xyz.com
# File:    user.py
# Project: notebook
# IDE:     PyCharm

from fastapi import APIRouter, Body, Depends

from ..dependencies import auth_depend
from ..libs.db_lib import db
from ..models.user import UserInDB
from ..schemas.user import UserInfo, UserSignUp
from ..utils import hash_tool

router = APIRouter(prefix='/user', tags=['用户接口'])


@router.post("/signup", summary="注册接口")
def signup(form_data: UserSignUp = Body(...)):
    # 拿到前端传过来的数据
    username = form_data.username
    password = form_data.password
    # 校验数据
    pass
    # 根据用户名去数据库里面查对应的 user
    user = db.get_or_none(username)
    # 如果已经有了，就返回错误信息
    if user is not None:
        return {"msg": "当前用户名已经被占用了"}
    # 保存到数据库
    encode_pwd = hash_tool.encrypt_password(password)
    user = UserInDB(username=username, password=encode_pwd)
    db.save(user)
    # 给前端响应信息
    return {'msg': "ok"}


@router.post("/login", summary="登陆接口")
def login():
    return {"msg": "login"}


@router.get("/me", summary="个人信息")
def get_my_info(me: UserInDB = Depends(auth_depend)):
    user_info = UserInfo(**me.dict())
    return {"msg": user_info}


@router.get("/vip", summary="查看 VIP 信息", dependencies=[Depends(auth_depend)])
def get_vip_info():
    return {"msg": "vip info"}
