# FastAPI In-Memory Rate Limiter

A pure Python, in-memory rate limiting dependency for FastAPI applications.

## Features
- **Sliding window algorithm** for precise rate limiting.
- **Zero external dependencies** (No Redis or external DBs required).
- **Automatic background memory cleanup** to prevent memory leaks by pruning expired data.
- **FastAPI dependency injection support** for easy integration.
- **Returns 429 Too Many Requests** status code when limits are exceeded.

## Requirements
- FastAPI
- Uvicorn

## Installation
Currently, this is a local module. You can copy the `src/rate_limiter` and `src/core` directories into your project.

```bash
pip install fastapi uvicorn
```

## Usage Example

### 1. Integration in FastAPI
Import the `limiter` instance and use it as a dependency. You should also start the background cleanup task during the application startup.

```python
from fastapi import FastAPI, Depends
from src.rate_limiter.limiter import limiter

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Start the cleanup background task to prune memory
    limiter.start_cleanup()

@app.on_event("shutdown")
async def shutdown():
    # Stop the cleanup background task
    limiter.stop_cleanup()

@app.get("/", dependencies=[Depends(limiter)])
async def root():
    return {"message": "Hello World"}
```

### 2. Custom Configuration
You can customize the rate limit and window size when initializing the `RateLimiter`:

```python
from src.rate_limiter.limiter import RateLimiter

# 50 requests per 30 seconds
custom_limiter = RateLimiter(requests_limit=50, window_seconds=30)
```

## Configuration
The `RateLimiter` class accepts the following parameters:
- `requests_limit`: Maximum number of requests allowed within the window (default: `100`).
- `window_seconds`: The duration of the sliding window in seconds (default: `60`).

## Project Structure
- `src/rate_limiter/limiter.py`: Core logic for the sliding window and cleanup task.
- `src/core/errors.py`: Custom HTTP 429 exception.
- `src/main.py`: Example FastAPI application demonstrating usage.
- `tests/test_rate_limiter.py`: Unit tests for the rate limiter.
