#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-10-13 14:46
# Author:  rongli
# Email:   abc@xyz.com
# File:    oauth.py
# Project: notebook
# IDE:     PyCharm
from urllib.parse import urlencode
from uuid import uuid4

import requests


class FastApiOauth:
    def __init__(self, authorization_url: str, token_url: str, profile_url: str, client_id: str, client_secret: str,
                 redirect_uri: str):
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.profile_url = profile_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @property
    def auth_url(self):
        query_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "read",
            "state": uuid4().hex
        }
        return f"{self.authorization_url}?{urlencode(query_params)}"

    def get_token(self, code, state):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        res = requests.post(self.token_url, data=data)
        return res.json()['access_token']

    def get_user_info(self, token):
        res = requests.get(self.profile_url, headers={"Authorization": "bearer " + token})
        return res.json()
