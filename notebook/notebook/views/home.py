#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:34
# Author:  rongli
# Email:   abc@xyz.com
# File:    home.py
# Project: notebook
# IDE:     PyCharm

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix='/home')


@router.get("")
def home():
    return HTMLResponse("<h1> home</h1>")
