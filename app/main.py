from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.dependencies import Base, engine

# Import all models to register them with SQLAlchemy
import app.models  # noqa

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for Unisphere - Campus Life Hub Mobile App",
    debug=settings.debug
)

# CORS Middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Unisphere API", "version": settings.app_version}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.app_name}


# Include API routers
from app.routes.v1 import auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])

# TODO: Include other routers
# from app.routes.v1 import courses, events, study_groups, announcements, locations
# app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])
# app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
# app.include_router(study_groups.router, prefix="/api/v1/study-groups", tags=["study-groups"])
# app.include_router(announcements.router, prefix="/api/v1/announcements", tags=["announcements"])
# app.include_router(locations.router, prefix="/api/v1/locations", tags=["locations"])


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}