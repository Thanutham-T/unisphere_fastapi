# Makefile for FastAPI project

# =========================
# Variables
# =========================
POETRY := poetry
DOCKER_COMPOSE := docker-compose

# =========================
# Help
# =========================
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make dev           # Run FastAPI locally with Poetry"
	@echo "  make prod-up       # Start Docker Compose in production mode (scaled)"
	@echo "  make prod-down     # Stop Docker Compose in production"
	@echo "  make test          # Run pytest"
	@echo "  make test-cov-up   # Start Docker Compose for testing"
	@echo "  make test-cov-down # Stop Docker Compose for testing"

# =========================
# Development
# =========================
.PHONY: dev
dev:
	$(POETRY) run fastapi dev unisphere/main.py

# =========================
# Production
# =========================
.PHONY: prod-up
prod-up:
	$(DOCKER_COMPOSE) --env-file ./.env.prod -f ./docker-compose.prod.yml up -d --scale unisphere-prod=2

.PHONY: prod-down
prod-down:
	$(DOCKER_COMPOSE) --env-file ./.env.prod -f ./docker-compose.prod.yml down -v

# =========================
# Testing
# =========================
.PHONY: test
test:
	$(POETRY) run pytest -v

.PHONY: test-cov-up
test-cov-up:
	$(DOCKER_COMPOSE) -f ./docker-compose.test.yml up -d

.PHONY: test-cov-down
test-cov-down:
	$(DOCKER_COMPOSE) -f ./docker-compose.test.yml down -v
