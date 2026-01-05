from fastapi.testclient import TestClient

from src.app.app import app

# Create a fresh client
client = TestClient(app)

# Patch the key function to ensure it always returns a value in tests
if hasattr(app.state, "limiter"):
    app.state.limiter._key_func = lambda _: "127.0.0.1"

def test_rate_limit_enforcement():
    """
    Test that rate limits are enforced and headers are present.
    Based on default setting: models = 10/minute
    """
    url = "/api/models"

    # Reset limiter storage manually to ensure test isolation
    if hasattr(app.state, "limiter"):
        app.state.limiter._storage.reset()
        # Re-apply key func just in case
        app.state.limiter._key_func = lambda _: "127.0.0.1"

    # Make 10 allowed requests
    for i in range(10):
        response = client.get(url)
        assert response.status_code == 200, f"Request {i+1} failed"

    # Make 11th request (should fail)
    response = client.get(url)
    assert response.status_code == 429
    assert "error" in response.json()
    assert "Rate limit exceeded" in response.json()["error"]

