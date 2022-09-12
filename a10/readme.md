# 后台任务

## 后台发邮件的简单演示

```python
async def send_email(email: str, msg: str):
    await asyncio.sleep(1)
    print(datetime.datetime.now())
    print(f"send email to {email}, {msg=}")


@app.get("/")
def task(bgt: BackgroundTasks):
    bgt.add_task(send_email, "1@q.cn", "hello")
    return {"now": datetime.datetime.now()}
```

## 封装成依赖项类

```python
class Scheduler:
    def __init__(self, store=None):
        self.store = store
        self.bgt = None
        self.func = None
        self.task = None
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
                await asyncio.sleep(1)
                if datetime.datetime.now() >= time_point:
                    break
            await self.func(*args, **kwargs)
            print(f"task run at {datetime.datetime.now()}")

        self.task = task_at
        await self.run()

    async def every(self, seconds: int, end_time: Optional[datetime.datetime] = None, count: Optional[int] = None):
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
```

调用方法

```python
@app.get("/class", summary="封装成依赖项类")
async def task(s: Scheduler = Depends(Scheduler())):
    # await s.bind(send_email, "1@q.cn", "hello run").run()  # 立即执行
    # await s.bind(send_email, "1@q.cn", "hello delay").delay(3)  # 延时执行
    # new_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    # await s.bind(send_email, "1@q.cn", "hello at").at(new_time)  # 固定时间点执行
    # await s.bind(send_email, "1@q.cn", "hello every").every(2, count=3)  # 周期执行
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    await s.bind(send_email, "1@q.cn", "hello every").every(2, end_time=end_time)  # 周期执行
    print(f"response  {datetime.datetime.now()}")
    return {"now": datetime.datetime.now()}
```