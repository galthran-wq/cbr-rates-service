from unittest.mock import AsyncMock

import httpx
import pytest
from httpx import AsyncClient
from src.dependencies import get_http_client
from src.main import app
from src.services import cbr

CBR_RESPONSE = {
    "Date": "2026-02-13T11:30:00+03:00",
    "PreviousDate": "2026-02-12T11:30:00+03:00",
    "Valute": {
        "USD": {
            "ID": "R01235",
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 92.5,
            "Previous": 92.3,
        },
        "EUR": {
            "ID": "R01239",
            "NumCode": "978",
            "CharCode": "EUR",
            "Nominal": 1,
            "Name": "Евро",
            "Value": 100.1,
            "Previous": 99.8,
        },
    },
}


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    cbr._cache = None
    cbr._cache_ts = 0.0


def _cbr_response() -> httpx.Response:
    return httpx.Response(200, json=CBR_RESPONSE, request=httpx.Request("GET", "https://test"))


@pytest.fixture()
def mock_client() -> AsyncMock:
    mock = AsyncMock(spec=httpx.AsyncClient)
    mock.get.return_value = _cbr_response()
    app.dependency_overrides[get_http_client] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


async def test_get_rates(client: AsyncClient, mock_client: AsyncMock) -> None:
    response = await client.get("/rates")
    assert response.status_code == 200
    data = response.json()
    assert "USD" in data["rates"]
    assert "EUR" in data["rates"]
    assert data["rates"]["USD"]["value"] == 92.5
    assert data["rates"]["USD"]["nominal"] == 1


async def test_get_rate(client: AsyncClient, mock_client: AsyncMock) -> None:
    response = await client.get("/rates/usd")
    assert response.status_code == 200
    data = response.json()
    assert data["rate"]["char_code"] == "USD"
    assert data["rate"]["value"] == 92.5
    assert data["rate"]["previous"] == 92.3


async def test_get_rate_case_insensitive(client: AsyncClient, mock_client: AsyncMock) -> None:
    response = await client.get("/rates/UsD")
    assert response.status_code == 200
    assert response.json()["rate"]["char_code"] == "USD"


async def test_get_rate_not_found(client: AsyncClient, mock_client: AsyncMock) -> None:
    response = await client.get("/rates/XYZ")
    assert response.status_code == 404


async def test_get_rates_cbr_unavailable(client: AsyncClient, mock_client: AsyncMock) -> None:
    mock_client.get.side_effect = httpx.ConnectError("connection refused")
    response = await client.get("/rates")
    assert response.status_code == 502


async def test_get_rates_cached(client: AsyncClient, mock_client: AsyncMock) -> None:
    await client.get("/rates")
    await client.get("/rates")
    mock_client.get.assert_called_once()
