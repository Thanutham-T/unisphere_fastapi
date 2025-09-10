# Unisphere FastAPI

This project is a backend that provides API for campus life hub mobile app using FastAPI.

## Prerequisites

- Python 3.12+
- Poetry (Python dependency management)

## Setup Instructions

### 1. Install Poetry (if not already installed)

```bash
pip install poetry
```

### 2. Install Dependencies

```bash
poetry install
```

## Running the Application

### Development Mode

You can run the FastAPI development server using the provided script:

```bash
./scripts/run-api-dev
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
unisphere_fastapi/
├── scripts/
│   └── run-api-dev          # Development server script
├── unisphere/
│   ├── __init__.py
│   └── main.py              # FastAPI application entry point
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Poetry lock file
└── README.md
```

## Development

### Adding New Dependencies

```bash
poetry add package_name
```

### Adding Development Dependencies

```bash
poetry add --group dev package_name
```