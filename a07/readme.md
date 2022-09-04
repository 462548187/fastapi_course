# 把一个类作为依赖项来使用

> 可配置，更灵活

```python
class FolderMaker:
    def __init__(self, upload_to: str = ''):
        self.upload_to = upload_to

    def __call__(self):
        dir_path = media_dir / self.upload_to
        # 检查目录存不存在等等
        return str(dir_path)
```

```python
dir_name: FolderMaker = Depends(FolderMaker("image"))
```