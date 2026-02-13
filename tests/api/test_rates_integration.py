from collections.abc import AsyncIterator

import httpx
import pytest
from httpx import AsyncClient
from src.dependencies import get_http_client
from src.main import app
from src.services import cbr


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    cbr._cache = None
    cbr._cache_ts = 0.0


@pytest.fixture(autouse=True)
async def _live_http_client() -> AsyncIterator[None]:
    async with httpx.AsyncClient() as client:
        app.dependency_overrides[get_http_client] = lambda: client
        yield
        app.dependency_overrides.clear()


@pytest.mark.integration
async def test_get_rates_live(client: AsyncClient) -> None:
    response = await client.get("/rates")
    assert response.status_code == 200
    data = response.json()
    assert "date" in data
    assert "rates" in data
    assert len(data["rates"]) > 0
    usd = data["rates"]["USD"]
    assert usd["char_code"] == "USD"
    assert usd["nominal"] == 1
    assert usd["value"] > 0
    assert usd["previous"] > 0
    assert isinstance(usd["num_code"], str)
    assert isinstance(usd["name"], str)


@pytest.mark.integration
async def test_get_rate_usd_live(client: AsyncClient) -> None:
    response = await client.get("/rates/usd")
    assert response.status_code == 200
    data = response.json()
    assert data["rate"]["char_code"] == "USD"
    assert data["rate"]["value"] > 0


@pytest.mark.integration
async def test_get_rate_not_found_live(client: AsyncClient) -> None:
    response = await client.get("/rates/XYZ")
    assert response.status_code == 404


@pytest.mark.integration
async def test_get_rates_structure_live(client: AsyncClient) -> None:
    response = await client.get("/rates")
    data = response.json()
    for code, rate in data["rates"].items():
        assert code == rate["char_code"]
        assert rate["nominal"] >= 1
        assert rate["value"] > 0
        assert rate["previous"] > 0
        assert len(rate["num_code"]) == 3
