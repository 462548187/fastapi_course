#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-03 13:44
# Author:  rongli
# Email:   abc@xyz.com
# File:    hashlib.py
# Project: fastapi_course
# IDE:     PyCharm
from passlib.handlers.pbkdf2 import pbkdf2_sha256


class Hash:
    @staticmethod
    def encrypt_password(raw_password: str) -> str:
        """
        加密密码
        :param raw_password: 明文密码
        :return: 加密后的密文密码
        """
        return pbkdf2_sha256.hash(raw_password)

    @staticmethod
    def check_password(hash_password: str, raw_password: str) -> bool:
        """
        密码验证
        :param hash_password: 密文密码
        :param raw_password:  明文密码
        :return: 通过返回真，不通过返回假
        """
        return pbkdf2_sha256.verify(raw_password, hash_password)
