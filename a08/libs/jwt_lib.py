#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 15:27
# Author:  rongli
# Email:   abc@xyz.com
# File:    jwt.py
# Project: fastapi_course
# IDE:     PyCharm
import json


class Token:
    @staticmethod
    def encode(payload):
        return json.dumps(payload)[::-1]

    @staticmethod
    def decode(token: str):
        print(token)
        token = token.replace("\\","")
        payload = json.loads(token[::-1])
        if not isinstance(payload, dict):
            raise ValueError("payload 格式错误")
        return payload


token_tool = Token()

if __name__ == '__main__':
    payload = {"username": "tom"}
    token = token_tool.encode(payload)
    print(token)
    print(token_tool.decode(token))
