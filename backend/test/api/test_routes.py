import unittest
from httpx import AsyncClient, ASGITransport

from src.app.app import app


class TestRoutes(unittest.IsolatedAsyncioTestCase):
    """Test API routes."""
    
    async def asyncSetUp(self):
        self.app = app

    async def test_new_game(self):
        """Test the /new endpoint returns a valid 4x4 grid."""
        async with AsyncClient(transport=ASGITransport(app=self.app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/new",
                json={"difficulty": "easy"}
            )

        self.assertEqual(response.status_code, 200)
        grid = response.json()
        self.assertEqual(len(grid), 4)
        for row in grid:
            self.assertEqual(len(row), 4)

    async def test_move_valid(self):
        """Test the /move endpoint with a valid move."""
        initial_grid = [
            [2, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        async with AsyncClient(transport=ASGITransport(app=self.app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/move",
                json={"grid": initial_grid, "direction": "right", "turns": 10}
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("grid", data)
        self.assertIn("status", data)
        self.assertIn("largest_number", data)
        self.assertIn("turns", data)
        self.assertEqual(data["turns"], 11)

        self.assertEqual(data["grid"][0][3], 2)

    async def test_move_invalid_direction(self):
        """Test the /move endpoint with an invalid direction."""
        initial_grid = [[None]*4]*4
        async with AsyncClient(transport=ASGITransport(app=self.app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/move",
                json={"grid": initial_grid, "direction": "sideways", "turns": 0}
            )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid direction", response.json()["detail"])

    async def test_recommend(self):
        """Test the /recommend endpoint."""
        grid = [[2, None, None, None], [None]*4, [None]*4, [None]*4]
        async with AsyncClient(transport=ASGITransport(app=self.app), base_url="http://test") as ac:
            response = await ac.post(
                "/api/recommend",
                json={"grid": grid, "provider": "heuristic", "model": "simple"}
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("suggested_move", data)
        self.assertIn("rationale", data)
        self.assertIn("predicted_grid", data)


if __name__ == "__main__":
    unittest.main()
