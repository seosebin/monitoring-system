from fastapi import FastAPI
import logging
import time

app = FastAPI()


# 일반 API
@app.get("/")
def home():
    ...

@app.get("/health")
def health():
    ...

@app.get("/users")
def users():
    ...

# 장애 실험 API
@app.get("/error")
def error():
    ...

@app.get("/slow")
def slow():
    ...

@app.get("/analytics/heavy")
def heavy():
    ...

@app.get("/cache/load")
def cache_load():
    ...