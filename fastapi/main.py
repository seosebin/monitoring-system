from fastapi import FastAPI, Request, HTTPException
import logging
import time
from collections import deque

app = FastAPI()

memory_store = deque(maxlen=100)

cache = {}

access_logger = logging.getLogger("access_logger")
error_logger = logging.getLogger("error_logger")

access_logger.setLevel(logging.INFO)
error_logger.setLevel(logging.ERROR)

access_handler = logging.FileHandler("/app/logs/access.log")
error_handler = logging.FileHandler("/app/logs/error.log")

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

access_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

access_logger.addHandler(access_handler)
error_logger.addHandler(error_handler)

def write_access_log(request: Request, status_code: int, response_time:float):
    access_logger.info(
        f"method={request.method} path={request.url.path} "
        f"status={status_code} response_time={response_time}"
    )

def write_error_log(request: Request, status_code: int, error_message: str):
    error_logger.error(
        f"method={request.method} path={request.url.path} "
        f"status={status_code} error={error_message}"
    )


# 일반 API
@app.get("/")
def home(request:Request):
    start = time.time()

    response = {"message": "Monitoring Project"}

    response_time = round(time.time() - start, 4)
    write_access_log(request, 200, response_time)

    return response

@app.get("/health")
def health(request: Request):
    start = time.time()

    response = {"status": "ok"}

    response_time = round(time.time() - start, 4)
    write_access_log(request, 200, response_time)

    return response

@app.get("/users")
def users(request: Request):
    start = time.time()

    response = {
        "users": [
            {"id": 1, "name": "kim"},
            {"id": 2, "name": "lee"},
        ]
    }

    response_time = round(time.time() - start, 4)
    write_access_log(request, 200, response_time)

    return response

# 장애 실험 API
@app.get("/error")
def error(request: Request):
    start = time.time()

    try:
        raise Exception("Test Exception")
    except Exception as e:
        response_time = round(time.time() - start, 4)

        write_access_log(request, 500, response_time)
        write_error_log(request, 500, str(e))
        
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/slow")
def slow(request: Request):
    start = time.time()

    time.sleep(5)

    response_time = round(time.time() - start, 4)
    write_access_log(request, 200, response_time)

    return {
        "message": "slow response",
        "response_time": response_time
    }

@app.get("/analytics/heavy")
def heavy(request: Request):
    start = time.time()

    if "heavy_result" in cache:
        response_time = round(time.time() - start, 4)

        write_access_log(request, 200, response_time)
        access_logger.info("CACHE HIT")

        return {
            "message": "heavy analytics",
            "cache": "hit",
            "response_time": response_time
        }

    result = 0
    for i in range(80_000_000):
        result += i * i
    
    cache["heavy_result"] = result

    response_time = round(time.time() - start, 4)

    write_access_log(request, 200, response_time)
    access_logger.info("CACHE HIT")

    return {
        "message": "heavy analytics",
        "cache": "miss",
        "response_time": response_time
    }

@app.get("/cache/load")
def cache_load(request:Request):
    start = time.time()

    data = "x" * 10_000_000
    memory_store.append(data)

    if len(memory_store) > 100:
        memory_store.clear()

    response_time = round(time.time() - start, 4)
    write_access_log(request, 200, response_time)

    return {
        "message": "cache loaded",
        "cache_count": len(memory_store),
        "response_time": response_time
    }