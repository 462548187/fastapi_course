#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-10-13 14:46
# Author:  rongli
# Email:   abc@xyz.com
# File:    __init__.py.py
# Project: notebook
# IDE:     PyCharm

from .oauth import FastApiOauth
from ..config import settings

fast_oauth = FastApiOauth(
        authorization_url=settings.oauth_authorization_url,
        token_url=settings.oauth_token_url,
        profile_url=settings.oauth_profile_url,
        client_id=settings.oauth_client_id,
        client_secret=settings.oauth_client_secret,
        redirect_uri=settings.oauth_redirect_uri
)
