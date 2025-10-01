from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status

from unisphere.routes.v1.auth_router import get_current_user
from unisphere.schemas.upload_schema import UploadResponse
from unisphere.schemas.user_schema import User as SchemaUser
from unisphere.services.upload_service import UploadService

router = APIRouter(prefix="/upload", tags=["upload"])


def get_upload_service() -> UploadService:
    return UploadService()


@router.post("/image", response_model=UploadResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    upload_service: UploadService = Depends(get_upload_service),
    _: SchemaUser = Depends(get_current_user)  # Just for authentication
):
    """Upload an image file"""
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )

        # Check file size (10MB limit)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10MB"
            )

        # Save the file
        file_path = await upload_service.save_image(file)

        # Generate full URL
        base_url = str(request.base_url).rstrip('/')
        file_url = f"{base_url}/{file_path}"

        return UploadResponse(
            message="File uploaded successfully",
            url=file_url,
            filename=file.filename
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        ) from e


@router.get("/image/{filename}")
async def get_image(
    filename: str,
    request: Request
):
    """Get an uploaded image"""
    try:
        # Check if file exists in the images directory
        image_path = f"uploads/images/{filename}"
        file_path = Path(image_path)

        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )

        # Return the static file URL
        base_url = str(request.base_url).rstrip('/')
        return {"url": f"{base_url}/{image_path}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get file: {str(e)}"
        ) from e


@router.delete("/image/{filename}")
async def delete_image(
    filename: str,
    upload_service: UploadService = Depends(get_upload_service),
    _: SchemaUser = Depends(get_current_user)  # Just for authentication
):
    """Delete an uploaded image"""
    try:
        # Construct the image path
        image_path = f"uploads/images/{filename}"

        # Use the upload service to delete the image
        success = upload_service.delete_image(image_path)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found or could not be deleted"
            )

        return {"message": "File deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {str(e)}"
        ) from e
