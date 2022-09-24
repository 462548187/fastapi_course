# 官方文档给的示例太难了

https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/

Authorization: bearer header.payload.sign

# 如何使用“小锁”

## 第一步：

获取 token 方法改为

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token: str = Depends(oauth2_scheme)
```

## 第二步

`tokenUrl` 指向的地址要能返回

```json
{
    "access_token": "token",
    "token_type": "bearer"
}
```

获取表单数据时，可以使用

```python
form_data: OAuth2PasswordRequestForm = Depends()
```

# 使用真正的 hash库、jwt库

## 安装

```shell
pip install passlib
pip install python-jose[cryptography]
```

## 替换加密解密的哈希算法

```python
# check_password
pbkdf2_sha256.verify(raw_password, hash_password)

# encrypt_password
pbkdf2_sha256.hash(raw_password)
```

## 替换 jwt 加密 解密算法

```python
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_exp_seconds)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt
```

```python
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except (jwt.ExpiredSignatureError,JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token已失效，请重新登陆！",
            headers={"WWW-Authenticate": "Bearer"})
```