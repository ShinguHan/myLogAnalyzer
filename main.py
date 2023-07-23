from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 'static' 디렉토리의 파일을 '/static' URL 경로를 통해 제공합니다.
app.mount("/static", StaticFiles(directory="static"), name="static")
