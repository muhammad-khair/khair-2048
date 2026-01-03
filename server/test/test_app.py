import pytest
from httpx import AsyncClient, ASGITransport
from server.src.app import app


@pytest.mark.asyncio
async def test_new_game():
    """Test the /new endpoint returns a valid 4x4 grid."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/new")
    
    assert response.status_code == 200
    grid = response.json()
    assert len(grid) == 4
    for row in grid:
        assert len(row) == 4


@pytest.mark.asyncio
async def test_move_valid():
    """Test the /move endpoint with a valid move."""
    initial_grid = [
        [2, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/move", json={"grid": initial_grid, "direction": "right"})
    
    assert response.status_code == 200
    data = response.json()
    assert "grid" in data
    assert "status" in data
    assert "largest_number" in data
    
    # After moving right, the first row should have 2 at the end
    assert data["grid"][0][3] == 2


@pytest.mark.asyncio
async def test_move_invalid_direction():
    """Test the /move endpoint with an invalid direction."""
    initial_grid = [[None]*4]*4
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/move", json={"grid": initial_grid, "direction": "sideways"})
    
    assert response.status_code == 400
    assert "Invalid direction" in response.json()["detail"]
