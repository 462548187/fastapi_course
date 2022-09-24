#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-24 21:02
# Author:  rongli
# Email:   abc@xyz.com
# File:    main.py.py
# Project: notebook
# IDE:     PyCharm

import uvicorn

from notebook.config import settings

if __name__ == '__main__':
    uvicorn.run("notebook.server:app",
                host=settings.server_host,
                port=settings.server_port,
                reload=True,
                reload_dirs=["notebook"])
