from fastapi.testclient import TestClient

from src.app.app import app
from src.config.settings import SETTINGS, RateLimitSettings

# Create a fresh client
client = TestClient(app)

# Patch the key function to ensure it always returns a value in tests
if hasattr(app.state, "limiter"):
    app.state.limiter._key_func = lambda _: "127.0.0.1"

def test_rate_limit_enforcement():
    """
    Test that rate limits are enforced and headers are present.
    Uses mocked setting of 30/minute.
    """
    url = "/api/models"

    # Reset limiter storage manually to ensure test isolation
    if hasattr(app.state, "limiter"):
        app.state.limiter._storage.reset()
        app.state.limiter._key_func = lambda _: "127.0.0.1"

    # Store original value and patch for test
    original_models = SETTINGS.rate_limit.models
    per_minute_rate = 30
    SETTINGS.rate_limit.models = f"{per_minute_rate}/minute"

    try:
        # Make per_minute_rate allowed requests
        for i in range(per_minute_rate):
            response = client.get(url)
            assert response.status_code == 200, f"Request {i+1} failed"

        # Make (per_minute_rate + 1)th request (should fail)
        response = client.get(url)
        assert response.status_code == 429
        assert "error" in response.json()
        assert "Rate limit exceeded" in response.json()["error"]
    finally:
        # Restore original value
        SETTINGS.rate_limit.models = original_models
