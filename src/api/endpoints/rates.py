from typing import Annotated

import httpx
from fastapi import APIRouter, Depends

from src.dependencies import get_http_client
from src.schemas.rates import RatesResponse, SingleRateResponse
from src.services.cbr import fetch_rate, fetch_rates

router = APIRouter(prefix="/rates")

HttpClient = Annotated[httpx.AsyncClient, Depends(get_http_client)]


@router.get("")
async def get_rates(client: HttpClient) -> RatesResponse:
    return await fetch_rates(client)


@router.get("/{char_code}")
async def get_rate(char_code: str, client: HttpClient) -> SingleRateResponse:
    return await fetch_rate(client, char_code)
