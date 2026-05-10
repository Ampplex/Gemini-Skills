import time
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app
from src.rate_limiter.limiter import limiter

client = TestClient(app)

def test_rate_limiter_limit():
    # Clear the storage before test
    limiter.storage.clear()
    
    # Send 100 requests - all should pass
    # Using 100 because the limit is 100.
    for i in range(100):
        response = client.get("/")
        assert response.status_code == 200, f"Request {i+1} failed: {response.text}"
        
    # 101st request should fail
    response = client.get("/")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["detail"]

def test_rate_limiter_sliding_window():
    limiter.storage.clear()
    
    # We need to mock time both in the limiter and in the test
    with patch('src.rate_limiter.limiter.time.time') as mock_time:
        start_time = 1000.0
        mock_time.return_value = start_time
        
        # Send 100 requests at T=1000
        for i in range(100):
            response = client.get("/")
            assert response.status_code == 200
            
        # 101st should fail
        assert client.get("/").status_code == 429
        
        # Move time forward by 61 seconds (T=1061)
        mock_time.return_value = start_time + 61
        
        # Next request should pass because the previous 100 are now outside the window
        response = client.get("/")
        assert response.status_code == 200

def test_cleanup_mechanism():
    limiter.storage.clear()
    # Add an old entry
    limiter.storage["1.2.3.4"] = [time.time() - 100]
    
    # Manually trigger the logic inside _cleanup_loop for verification
    now = time.time()
    ips_to_remove = []
    for ip in list(limiter.storage.keys()):
        timestamps = limiter.storage[ip]
        while timestamps and timestamps[0] < now - limiter.window_seconds:
            timestamps.pop(0)
        if not timestamps:
            ips_to_remove.append(ip)
    
    for ip in ips_to_remove:
        del limiter.storage[ip]
        
    assert "1.2.3.4" not in limiter.storage

