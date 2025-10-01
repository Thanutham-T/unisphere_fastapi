import uuid
from pathlib import Path
from typing import Optional

import aiofiles  # type: ignore[import-untyped]
from fastapi import UploadFile


class UploadService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

        # Create subdirectories
        self.images_dir = self.upload_dir / "images"
        self.images_dir.mkdir(exist_ok=True)

    def _validate_image_file(self, file: UploadFile) -> bool:
        """Validate if the uploaded file is a valid image"""
        # Check file extension
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        file_extension = Path(file.filename or "").suffix.lower()

        if file_extension not in allowed_extensions:
            return False

        # Check MIME type
        allowed_mime_types = {
            'image/jpeg', 'image/jpg', 'image/png',
            'image/gif', 'image/webp'
        }

        if file.content_type not in allowed_mime_types:
            return False

        return True

    def _generate_filename(self, original_filename: str) -> str:
        """Generate a unique filename"""
        file_extension = Path(original_filename).suffix.lower()
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_extension}"

    async def save_image(self, file: UploadFile, max_size_mb: int = 10) -> Optional[str]:
        """
        Save uploaded image file to server

        Args:
            file: The uploaded file
            max_size_mb: Maximum file size in MB

        Returns:
            Relative path to saved file or None if failed
        """
        if not self._validate_image_file(file):
            raise ValueError("Invalid image file type")

        # Check file size
        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)

        if file_size_mb > max_size_mb:
            raise ValueError(f"File size exceeds {max_size_mb}MB limit")

        # Reset file pointer
        await file.seek(0)

        # Generate unique filename
        filename = self._generate_filename(file.filename or "image")
        file_path = self.images_dir / filename

        try:
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)

            # Return relative path for URL construction
            return f"uploads/images/{filename}"

        except Exception as e:
            # Clean up if file was partially created
            if file_path.exists():
                file_path.unlink()
            raise RuntimeError(f"Failed to save file: {str(e)}") from e

    def delete_image(self, image_path: str) -> bool:
        """
        Delete image file from server

        Args:
            image_path: Relative path to the image file (e.g., "uploads/images/filename.jpg")

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            # Ensure path is within upload directory
            if not image_path.startswith("uploads/"):
                return False

            # Convert relative path to absolute path based on upload directory
            # Remove "uploads/" prefix and construct full path
            relative_to_upload = image_path[8:]  # Remove "uploads/" prefix
            file_path = self.upload_dir / relative_to_upload

            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                return True
            return False

        except OSError:
            return False

    def get_image_url(self, image_path: str, base_url: str) -> str:
        """
        Generate full URL for image

        Args:
            image_path: Relative path to image
            base_url: Base URL of the server

        Returns:
            Full URL to the image
        """
        return f"{base_url.rstrip('/')}/{image_path}"
