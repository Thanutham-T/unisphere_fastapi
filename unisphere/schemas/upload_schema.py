from typing import Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response model for file upload"""
    message: str
    url: str
    filename: Optional[str] = None
