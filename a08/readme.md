# 官方文档给的示例太难了

https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/

Authorization: bearer header.payload.sign

# 第一步
获取 token 方法改为
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token: str = Depends(oauth2_scheme)
```
# 第二步
`tokenUrl` 指向的地址要能返回 
```json
{"access_token": "token", "token_type": "bearer"}
```

获取表单数据时，可以使用
```python
form_data: OAuth2PasswordRequestForm = Depends()