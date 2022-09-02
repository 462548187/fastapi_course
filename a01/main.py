#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 09:08
# Author:  rongli
# Email:   abc@xyz.com
# File:    hello.py
# Project: fastapi_course
# IDE:     PyCharm
import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
