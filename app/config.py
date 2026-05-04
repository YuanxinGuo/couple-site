from pydantic_settings import BaseSettings
from datetime import date


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    secret_key: str
    site_password: str
    relationship_start_date: date
    database_url: str = "sqlite:///./data/couple.db"

    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    site_title: str = "我们的小窝"
    site_description: str = "记录我们的每一天"


settings = Settings()
