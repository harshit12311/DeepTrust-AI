"""Application configuration for DeepTrust AI."""

import os
from pathlib import Path


class Config:
    """Default settings used by the Flask application."""

    # Secret used by Flask to protect sessions and signed data.
    SECRET_KEY = os.getenv("SECRET_KEY", "deeptrust-ai-development-key")

    # MySQL server hostname or IP address.
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")

    # MySQL account username for the application database.
    MYSQL_USER = os.getenv("MYSQL_USER", "root")

    # MySQL account password; blank is suitable only for local development.
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

    # Name of the MySQL database used by DeepTrust AI.
    MYSQL_DB = os.getenv("MYSQL_DB", "deeptrust_ai")

    # Directory where uploaded image and video files are stored.
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER", str(Path(__file__).resolve().parent.parent / "uploads")
    )

    # Maximum permitted upload size: 50 MB.
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    # Image file types accepted by the application.
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}

    # Video file types accepted by the application.
    ALLOWED_VIDEO_EXTENSIONS = {"mp4", "avi", "mov"}
