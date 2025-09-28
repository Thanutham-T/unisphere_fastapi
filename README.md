# Unisphere FastAPI

This document provides a comprehensive guide for setting up and using the **Unisphere FastAPI** project with **VS Code Dev Containers**.

---

## 🚀 Quick Start

### Prerequisites

1. **VS Code** with the following extensions:
   - [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)  
   - [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

2. **Docker Desktop** installed and running

---

### Opening the Project in a Dev Container

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd unisphere_fastapi
```

2. **Open in VS Code**:

```bash
code .
```

3. **Open in Dev Container**:

- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)  
- Type **"Dev Containers: Reopen in Container"** and select it  
- Wait for the container to build  

**Alternative:** Click the "Reopen in Container" button if VS Code detects the `.devcontainer` folder.

---

## 📁 Project Structure

add `.env.dev` `.env.prod` `dbconfig` yourself

```
unisphere_fastapi/
├── .devcontainer/                # Development container setup
│   ├── .env.dev                  # [SETUP] Environment variables for development
│   ├── devcontainer.json         # Devcontainer configuration
│   ├── docker-compose.dev.yml    # Docker Compose for development
│   └── Dockerfile.dev            # Dockerfile for development environment
├── dbconfig/                     # Database configuration
│   └── redis.conf                # Redis config
├── nginx/                        # Nginx configuration
│   ├── cert/                     # Certificates for HTTPS (generate locally)
│   │   └── *.pem                 # Key and certificate files
│   └── conf/
│       └── tom.conf              # Nginx configuration file
├── scripts/                      # Shell scripts
│   ├── run-api-dev.sh            # Start development server
│   └── run-api-test.sh           # Start test server
├── tests/                        # Pytest tests
│   ├── __init__.py
│   ├── conftest.py               # Test configuration
│   └── ...
├── unisphere/                    # FastAPI application
│   ├── __init__.py               # App entry point
│   ├── main.py                   # FastAPI application
│   ├── core/                     # Core dependencies
│   │   ├── __init__.py
│   │   ├── config.py             # Configuration settings
│   │   ├── dependencies.py       # Dependency injection
│   │   └── security.py           # Security utilities
│   ├── models/                   # SQLModel ORM models
│   │   ├── __init__.py
│   │   └── ...
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   └── ...
│   ├── routes/                   # API routes
│   │   ├── __init__.py
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── health.py         # Health check endpoint
│   │       └── ...
│   └── services/                 # Business logic
│       ├── __init__.py
│       └── ...
├── uploads/                      # Directory for uploaded files
├── .env.prod                     # [SETUP] Environment variables for production
├── .dockerignore                 # Docker ignore file
├── .gitignore                    # Git ignore file
├── .gitattributes                # Git attributes
├── Dockerfile.test               # Dockerfile for testing
├── Dockerfile.prod               # Dockerfile for production
├── docker-compose.test.yml       # Docker Compose for testing
├── docker-compose.prod.yml       # Docker Compose for production
├── poetry.toml                   # Poetry configuration
├── pyproject.toml                # Python package management
├── poetry.lock                   # Poetry lock file
└── README.md                     # This file
```

---

## 🌐 API Endpoints

Once running, the following services are available:

- **FastAPI Application:** http://localhost:8000  
- **Swagger UI:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc  
- **PgAdmin:** http://localhost:5050
- **Nginx:** https://localhost (only production)

---

### 🎒 Database Configuration

**PostgreSQL:**

| Environment | User      | Password | Database           |
|------------|-----------|---------|------------------|
| Dev        | unidev    | unidev  | unisphere_dev_db |
| Test       | -         | -       | SQLite           |
| Prod       | -         | -       | unisphere_prod_db |

**Redis:**

- Password: assign yourself in `dbconfig/redis.conf`  

**PgAdmin:**

| User          | Password |
|---------------|---------|
| admin@admin.com | admin   |


### 📃 Makefile Usage

This Makefile helps you manage a FastAPI project locally and with Docker Compose.

##### Commands

- `make dev`  
  Run FastAPI locally using Poetry.

- `make prod-up`  
  Start Docker Compose in production mode with scaling.

- `make prod-down`  
  Stop Docker Compose in production and remove volumes.

- `make test`  
  Run tests using pytest.

- `make test-cov-up`  
  Start Docker Compose for testing.

- `make test-cov-down`  
  Stop Docker Compose used for testing and remove volumes.



### 🙏 Reference

- https://github.com/r202-coe-psu-tutorial/mdev-68