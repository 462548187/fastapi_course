# 路径操作装饰器依赖项
> 路径操作装饰器依赖项（以下简称为“路径装饰器依赖项”）的执行或解析方式和普通依赖项一样，但就算这些依赖项会返回值，**它们的值也不会传递给路径操作函数**。



```python
def auth_depend(auth: str = Header(..., description="请求头认证", alias="X-auth")):
    if auth != "admin":
        raise HTTPException(status_code=401, detail="认证不通过")


@app.get("/depends/auth", summary="路径操作装饰器依赖项", dependencies=[Depends(auth_depend)])
def auth_admin():
    return {"msg": "ok"}
```