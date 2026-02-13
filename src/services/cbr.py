import time

import httpx
import structlog

from src.config import settings
from src.core.exceptions import AppError
from src.schemas.rates import CurrencyRate, RatesResponse, SingleRateResponse

logger = structlog.get_logger()

_cache: RatesResponse | None = None
_cache_ts: float = 0.0


def _is_cache_valid() -> bool:
    return _cache is not None and (time.monotonic() - _cache_ts) < settings.cbr_cache_ttl


async def fetch_rates(client: httpx.AsyncClient) -> RatesResponse:
    global _cache, _cache_ts

    if _is_cache_valid():
        return _cache  # type: ignore[return-value]

    try:
        response = await client.get(settings.cbr_url)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error("cbr_request_failed", error=str(exc))
        if _cache is not None:
            logger.warning("cbr_serving_stale_cache")
            return _cache
        raise AppError(status_code=502, detail="Failed to fetch rates from CBR") from exc

    data = response.json()
    rates: dict[str, CurrencyRate] = {}

    for code, valute in data["Valute"].items():
        rates[code] = CurrencyRate(
            char_code=valute["CharCode"],
            num_code=valute["NumCode"],
            nominal=valute["Nominal"],
            name=valute["Name"],
            value=valute["Value"],
            previous=valute["Previous"],
        )

    _cache = RatesResponse(date=data["Date"], rates=rates)
    _cache_ts = time.monotonic()
    return _cache


async def fetch_rate(client: httpx.AsyncClient, char_code: str) -> SingleRateResponse:
    all_rates = await fetch_rates(client)
    code = char_code.upper()

    if code not in all_rates.rates:
        raise AppError(status_code=404, detail=f"Currency {code} not found")

    return SingleRateResponse(date=all_rates.date, rate=all_rates.rates[code])
