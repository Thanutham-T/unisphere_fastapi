from typing import List, Optional

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.core.config import get_settings
from unisphere.models import get_redis, get_session
from unisphere.schemas import greeting_schema
from unisphere.services.greeting_service.DBGreetingService import \
    DBGreetingService
from unisphere.services.greeting_service.GreetingServiceInterface import \
    GreetingServiceInterface
from unisphere.services.greeting_service.MockGreetingService import \
    MockGreetingService

router = APIRouter(prefix="/greetings", tags=["greetings"])


# Dependency to get service (mock or DB)
def get_greeting_service(session: AsyncSession = Depends(get_session)) -> GreetingServiceInterface:
    settings = get_settings()
    if settings.USE_MOCK:
        return MockGreetingService()
    return DBGreetingService(session=session)


# CRUD Endpoints
@router.get(
    "/",
    summary="List all greetings",
    description="Retrieve a list of all greetings.",
    response_model=List[greeting_schema.Greeting]
)
async def read_greetings(service: GreetingServiceInterface = Depends(get_greeting_service)) -> List[greeting_schema.Greeting]:
    greetings = await service.list_greetings()
    if not greetings:
        raise HTTPException(status_code=404, detail="No greetings found")
    return greetings


@router.get(
    "/{greeting_id}",
    summary="Get a specific greeting",
    description="Retrieve details of a specific greeting by ID.",
    response_model=greeting_schema.Greeting
)
async def read_greeting(greeting_id: int, service: GreetingServiceInterface = Depends(get_greeting_service)) -> Optional[greeting_schema.Greeting]:
    greeting = await service.get_greeting(greeting_id)
    if greeting is None:
        raise HTTPException(status_code=404, detail="Greeting not found")
    return greeting


@router.post(
    "/",
    summary="Create a new greeting",
    description="Create a new greeting.",
    response_model=greeting_schema.Greeting
)
async def create_greeting(greeting: greeting_schema.GreetingCreate, service: GreetingServiceInterface = Depends(get_greeting_service)) -> greeting_schema.Greeting:
    return await service.create_greeting(greeting)


@router.put(
    "/{greeting_id}",
    summary="Update a greeting",
    description="Update an existing greeting.",
    response_model=greeting_schema.Greeting
)
async def update_greeting(greeting_id: int, greeting: greeting_schema.GreetingUpdate, service: GreetingServiceInterface = Depends(get_greeting_service)) -> greeting_schema.Greeting:
    updated_greeting = await service.update_greeting(greeting_id, greeting)
    if updated_greeting is None:
        raise HTTPException(status_code=404, detail="Greeting not found")
    return updated_greeting


@router.delete(
    "/{greeting_id}",
    summary="Delete a greeting",
    description="Delete an existing greeting.",
    response_model=bool
)
async def delete_greeting(greeting_id: int, service: GreetingServiceInterface = Depends(get_greeting_service)) -> bool:
    deleted = await service.remove_greeting(greeting_id)
    return deleted is not None


@router.get("/redis/last-greeted")
async def last_greeted(redis_client: redis.Redis = Depends(get_redis)):
    name = await redis_client.get("last_greeted")
    return {"last_greeted": name}


@router.post("/redis/greet/{name}")
async def greet(name: str, redis_client: redis.Redis = Depends(get_redis)):
    await redis_client.set("last_greeted", name)
    return {"message": f"Hello, {name}!"}
