from datetime import datetime

from pydantic import BaseModel


class CurrencyRate(BaseModel):
    char_code: str
    num_code: str
    nominal: int
    name: str
    value: float
    previous: float


class RatesResponse(BaseModel):
    date: datetime
    rates: dict[str, CurrencyRate]


class SingleRateResponse(BaseModel):
    date: datetime
    rate: CurrencyRate
