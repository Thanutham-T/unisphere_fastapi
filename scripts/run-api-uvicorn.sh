#!/bin/bash
poetry run uvicorn unisphere.main:app --host 0.0.0.0 --port 8000 --reload