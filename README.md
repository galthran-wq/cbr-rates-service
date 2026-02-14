# CBR Rates Service

[![CI](https://github.com/galthran-wq/cbr-rates-service/actions/workflows/ci.yml/badge.svg)](https://github.com/galthran-wq/cbr-rates-service/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/galthran-wq/cbr-rates-service/badge.svg?branch=master)](https://coveralls.io/github/galthran-wq/cbr-rates-service?branch=master)
![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type_checker-mypy-blue)](https://mypy-lang.org/)

Microservice that provides exchange rates from the Central Bank of Russia (CBR).

## Stack

- **FastAPI** — async web framework
- **uv** — package manager
- **httpx** — async HTTP client
- **Pydantic v2** — validation and settings
- **structlog** — structured logging (JSON in production)
- **Prometheus** — metrics via prometheus-fastapi-instrumentator
- **pytest + httpx** — testing
- **ruff** — linting and formatting
- **mypy** — type checking
- **Docker** — containerization

## Quick Start

```bash
make install
make run
```

## API

### `GET /rates`

Returns all CBR exchange rates for today.

```bash
curl http://localhost:8000/rates
```

### `GET /rates/{char_code}`

Returns a single currency rate by code (case-insensitive).

```bash
curl http://localhost:8000/rates/usd
```

### `GET /health`

Health check endpoint.

### `GET /ready`

Readiness check endpoint.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `python-service-template` | Application name |
| `DEBUG` | `false` | Debug mode (console logs when true, JSON logs when false) |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `LOG_LEVEL` | `info` | Log level |
| `CORS_ORIGINS` | `["*"]` | Allowed CORS origins |
| `METRICS_ENABLED` | `true` | Enable Prometheus metrics |
| `CBR_URL` | `https://www.cbr-xml-daily.ru/daily_json.js` | CBR API endpoint |
| `CBR_CACHE_TTL` | `3600` | Rate cache TTL in seconds |

## Commands

| Command | Description |
|---|---|
| `make install` | Install dependencies |
| `make run` | Run dev server with hot reload |
| `make test` | Run tests with coverage |
| `make lint` | Run ruff + mypy |
| `make format` | Auto-format code |
| `make pre-commit` | Install pre-commit hooks |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run Docker container |

## Testing

```bash
make test                                    # all tests
uv run pytest -m "not integration"           # unit tests only
uv run pytest -m integration                 # integration tests only (hits real CBR API)
```

## Project Structure

```
src/
├── main.py           — app factory, structlog config, Prometheus setup
├── config.py         — pydantic-settings based configuration
├── dependencies.py   — FastAPI dependency injection providers
├── api/
│   ├── router.py     — aggregated API router
│   └── endpoints/    — route handlers
├── schemas/          — Pydantic request/response models
├── services/         — business logic layer
└── core/
    ├── exceptions.py — custom exceptions + handlers
    └── middleware.py  — CORS, request logging, request ID
```
