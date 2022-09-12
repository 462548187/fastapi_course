# 中间件的简单演示

## 一个记录时间的中间件

```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## 消费 request 的 body

```python
data = await request.body()

async def request_body():
     return {'type': 'http.request', 'body': data, 'more_body': False}

request = Request(request.scope, request_body)
```

## 获取请求的参数

```python
print(request.headers['host'])
print(request.url)
```

## 拿到响应的 body

```python
body_data = []

async def response_body():
    for data in body_data:
        yield data
    yield b""

async for chunk in response.body_iterator:
    if not isinstance(chunk, bytes):
        chunk = chunk.encode(response.charset)
    body_data.append(chunk)
    print(chunk)
response = StreamingResponse(status_code=response.status_code,
                             content=response_body(),
                             headers=dict(response.headers))
```

## 提前返回

```python
# 在 call_next 之前
if request.url.path == "/":
    return JSONResponse({"msg": "bye~"}, status_code=400)
```

> 注意：此处 JSONResponse 的 context 参数必须支持 json.dumps
>
> 如果需要传其他参数，可以调用 jsonable_encoder

## 简单封装一下

```python
class MiddlewareTest:
    def __init__(self, name: str):
        self.name = name

    async def test_order(self, request: Request, call_next):
        print(f"{self.name} start ")
        response = await call_next(request)
        print(f"{self.name} end ")
        return response

    def __call__(self, app: FastAPI):
        app.middleware("http")(self.test_order)


MiddlewareTest("m1")(app)
```

## 中间件的执行顺序

```python
MiddlewareTest("  m1")(app)
MiddlewareTest("m2")(app)
```

```shell
#m2 start 
#  m1 start 
#    hello
#  m1 end 
#m2 end
```

顺序：先注册的在内侧，洋葱模型