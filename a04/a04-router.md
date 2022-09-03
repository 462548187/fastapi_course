## 为什么要把路由分组？

为了方便管理

## 如何给路由分组？

先写好各个子路由

```python
from fastapi import APIRouter, Path

router = APIRouter(prefix='/user', tags=['用户管理'])


@router.get("", summary="查看用户列表")
def get_user_list():
    return 'user_list'


@router.get("/{uid}", summary="查看指定用户")
def get_one_user(uid: int = Path(...)):
    return f'get_one_user: {uid}'
```

在 main.py 中导入 router，并挂载它

```python
from .user import router as user_router
from .profile import router as profile_router

app.include_router(user_router)
app.include_router(profile_router)
```

## include_router 还可以配置什么？

```python
    def include_router(
        self,
        router: routing.APIRouter,
        *,
        prefix: str = "",
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        default_response_class: Type[Response] = Default(JSONResponse),
        callbacks: Optional[List[BaseRoute]] = None,
        generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> None:
```
