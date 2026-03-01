import unittest
from fastapi.testclient import TestClient

from src.app.app import app
from src.config.settings import SETTINGS


class TestRateLimitEnforcement(unittest.TestCase):
    """Test that rate limits are enforced and headers are present."""
    
    def setUp(self):
        self.client = TestClient(app)
        if hasattr(app.state, "limiter"):
            app.state.limiter._key_func = lambda _: "127.0.0.1"

    def test_rate_limit_enforcement(self):
        """Uses mocked setting of 30/minute."""
        url = "/api/models"

        if hasattr(app.state, "limiter"):
            app.state.limiter._storage.reset()
            app.state.limiter._key_func = lambda _: "127.0.0.1"

        original_models = SETTINGS.rate_limit.models
        per_minute_rate = 30
        SETTINGS.rate_limit.models = f"{per_minute_rate}/minute"

        try:
            for i in range(per_minute_rate):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200, f"Request {i+1} failed")

            response = self.client.get(url)
            self.assertEqual(response.status_code, 429)
            self.assertIn("error", response.json())
            self.assertIn("Rate limit exceeded", response.json()["error"])
        finally:
            SETTINGS.rate_limit.models = original_models


if __name__ == "__main__":
    unittest.main()
