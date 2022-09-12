#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Time:    2022-09-02 09:08
# Author:  rongli
# Email:   abc@xyz.com
# File:    hello.py
# Project: fastapi_course
# IDE:     PyCharm
import asyncio
import datetime
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.background import BackgroundTasks

from .docs import custom_docs

app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/static', StaticFiles(directory='static'))

custom_docs(app)


async def send_email(email: str, msg: str):
    print(f"send email to {email}, {msg=}, start at: {datetime.datetime.now()}")
    await asyncio.sleep(1)


class Scheduler:
    def __init__(self, store=None):
        self.store = store  # 未来可能要把任务持久化保存
        self.bgt = None  # BackgroundTasks
        self.func = None  # 任务函数
        self.task = None  # 实际执行的任务
        self.args = []
        self.kwargs = {}

    async def __call__(self, bgt: BackgroundTasks):
        self.bgt = bgt
        return self

    def bind(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        return self

    async def run(self):
        if self.task is None:
            self.task = self.func
        self.bgt.add_task(self.task, *self.args, **self.kwargs)

    async def delay(self, seconds: int):
        async def task_delay(*args, **kwargs):
            await asyncio.sleep(seconds)
            await self.func(*args, **kwargs)
            print(f"task run at {datetime.datetime.now()}, delay: {seconds}")

        self.task = task_delay
        await self.run()

    async def at(self, time_point: datetime.datetime):
        async def task_at(*args, **kwargs):
            while True:
                await asyncio.sleep(0.1)
                if datetime.datetime.now() >= time_point:
                    break
            await self.func(*args, **kwargs)
            print(f"task run at {datetime.datetime.now()}")

        self.task = task_at
        await self.run()

    async def every(self, seconds: int,
                    end_time: Optional[datetime.datetime] = None,
                    count: Optional[int] = None):
        async def task_every(*args, **kwargs):
            task_count = 0
            next_time = datetime.datetime.now()
            while True:
                if datetime.datetime.now() >= next_time:
                    next_time += datetime.timedelta(seconds=seconds)
                    await self.func(*args, **kwargs)
                    task_count += 1
                    while datetime.datetime.now() <= next_time:
                        await asyncio.sleep(0.1)

                if end_time is not None and datetime.datetime.now() >= end_time:
                    print(f"break at {datetime.datetime.now()}, {end_time=}")
                    break
                if count is not None and task_count >= count:
                    print(f"break at {datetime.datetime.now()},  {count=}")
                    break

        self.task = task_every
        await self.run()

    async def cron(self):
        """
        arq
        apscheduler
        celery
        """
        pass


@app.get("/task", summary="简单演示")
def task(bgt: BackgroundTasks):
    bgt.add_task(send_email, "1@q.cn", "hello")
    return {"now": datetime.datetime.now()}


@app.get("/class", summary="封装成依赖项类")
async def task(s: Scheduler = Depends(Scheduler())):
    # 后台立即执行
    # await s.bind(send_email, "1@q.cn", "hello run").run()
    # 延时执行
    # await s.bind(send_email, "1@q.cn", "hello delay").delay(3)
    # 固定时间点执行
    # new_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    # await s.bind(send_email, "1@q.cn", "hello at").at(new_time)
    # 周期执行
    # await s.bind(send_email, "1@q.cn", "hello every").every(2, count=3)
    # 周期执行
    # end_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    # await s.bind(send_email, "1@q.cn", "hello every").every(2, end_time=end_time)

    return {"now": datetime.datetime.now()}
