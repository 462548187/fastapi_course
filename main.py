import uvicorn

if __name__ == '__main__':
    uvicorn.run("temp.main:app", reload=True)
