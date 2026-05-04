import cloudinary
import cloudinary.uploader
from app.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


def upload_image(file_bytes: bytes, folder: str = "couple") -> dict:
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=folder,
        resource_type="image",
        transformation=[
            {"quality": "auto:good", "fetch_format": "auto"}
        ],
    )

    public_id = result["public_id"]
    return {
        "public_id": public_id,
        "url": cloudinary.CloudinaryImage(public_id).build_url(
            quality="auto:good", fetch_format="auto"
        ),
        "thumb_url": cloudinary.CloudinaryImage(public_id).build_url(
            width=600, height=600, crop="fill", gravity="auto",
            quality="auto:good", fetch_format="auto"
        ),
    }


def delete_image(public_id: str) -> None:
    cloudinary.uploader.destroy(public_id)

