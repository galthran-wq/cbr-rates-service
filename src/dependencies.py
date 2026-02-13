from collections.abc import AsyncIterator

import httpx
from fastapi import Request


async def get_http_client(request: Request) -> AsyncIterator[httpx.AsyncClient]:
    yield request.app.state.http_client
