"""Routes for uploading image and video files."""

from pathlib import Path

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from backend.config import Config
from backend.services.image_service import preprocess_image

# Blueprint that groups all upload-related endpoints.
upload_bp = Blueprint("upload", __name__)


def _is_allowed_file(filename: str) -> bool:
    """Return whether a filename has a supported image or video extension."""
    allowed_extensions = (
        Config.ALLOWED_IMAGE_EXTENSIONS | Config.ALLOWED_VIDEO_EXTENSIONS
    )
    extension = _get_file_extension(filename)
    return extension in allowed_extensions


def _is_image_file(filename: str) -> bool:
    """Return whether a filename has a supported image extension."""
    return _get_file_extension(filename) in Config.ALLOWED_IMAGE_EXTENSIONS


def _get_file_extension(filename: str) -> str:
    """Return the lowercase file extension without the leading dot."""
    if "." not in filename:
        return ""

    return filename.rsplit(".", 1)[1].lower()


@upload_bp.post("/upload")
def upload_file():
    """Save a supported file uploaded through the ``file`` form field."""
    uploaded_file = request.files.get("file")

    # A missing field or blank filename means the user did not select a file.
    if uploaded_file is None or not uploaded_file.filename:
        return jsonify(success=False, message="No file selected."), 400

    # Check the original filename before saving it to disk.
    if not _is_allowed_file(uploaded_file.filename):
        return jsonify(success=False, message="Unsupported file type."), 400

    filename = secure_filename(uploaded_file.filename)
    if not filename:
        return jsonify(success=False, message="Unsupported file type."), 400

    # Ensure the configured upload location is available before saving the file.
    upload_folder = Path(Config.UPLOAD_FOLDER)
    upload_folder.mkdir(parents=True, exist_ok=True)
    saved_file_path = upload_folder / filename
    uploaded_file.save(saved_file_path)

    file_type = "image" if _is_image_file(filename) else "video"

    if file_type == "image":
        processed_image = preprocess_image(str(saved_file_path))
        if processed_image is None:
            return jsonify(
                success=False,
                message="Image preprocessing failed.",
            ), 400

    return jsonify(
        success=True,
        filename=filename,
        file_type=file_type,
        message=f"{file_type.title()} upload successful.",
    )
