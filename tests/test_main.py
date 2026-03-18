import pytest
from httpx import AsyncClient
from main import app  # Импорт твоего FastAPI приложения

@pytest.mark.asyncio
async def test_read_main():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200