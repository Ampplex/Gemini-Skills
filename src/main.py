from fastapi import FastAPI, Depends
from src.rate_limiter.limiter import limiter

app = FastAPI(title="Rate Limited API")

@app.on_event("startup")
async def startup():
    # Start the cleanup background task
    limiter.start_cleanup()

@app.on_event("shutdown")
async def shutdown():
    # Stop the cleanup background task
    limiter.stop_cleanup()

@app.get("/", dependencies=[Depends(limiter)])
async def read_root():
    return {"message": "Hello World. You are not rate limited... yet."}

@app.get("/status")
async def status():
    return {
        "active_ips": len(limiter.storage),
        "limit": limiter.requests_limit,
        "window": limiter.window_seconds
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
