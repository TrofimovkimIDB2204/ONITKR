import pytest
from httpx import AsyncClient, ASGITransport # Добавили ASGITransport
from main import app 

@pytest.mark.asyncio
async def test_read_main():
    # Теперь передаем приложение через transport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200