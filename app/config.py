import os
from datetime import date


class Settings:
    def __init__(self):
        self.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
        self.site_password = os.environ.get("SITE_PASSWORD", "5201314")
        self.relationship_start_date = date.fromisoformat(
            os.environ.get("RELATIONSHIP_START_DATE", "2023-05-20")
        )
        self.database_url = os.environ.get("DATABASE_URL", "sqlite:///./data/couple.db")
        self.cloudinary_cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
        self.cloudinary_api_key = os.environ.get("CLOUDINARY_API_KEY", "")
        self.cloudinary_api_secret = os.environ.get("CLOUDINARY_API_SECRET", "")
        self.site_title = os.environ.get("SITE_TITLE", "我们的小窝")
        self.site_description = os.environ.get("SITE_DESCRIPTION", "记录我们的每一天")


settings = Settings()
