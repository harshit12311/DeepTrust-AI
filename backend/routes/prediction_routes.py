"""Routes for running deepfake predictions on uploaded files."""

from pathlib import Path

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from backend.config import Config
from backend.services.ai_service import predict_image, predict_video


# Blueprint that groups all prediction-related endpoints.
prediction_bp = Blueprint("prediction", __name__)


def _get_uploaded_file_path():
    """Validate the request body and return the uploaded file path."""
    data = request.get_json(silent=True)

    # Prediction requests must include the saved upload filename.
    if not data or not data.get("filename"):
        return None, (jsonify(success=False, message="Filename is required."), 400)

    filename = secure_filename(data["filename"])
    if not filename:
        return None, (jsonify(success=False, message="Invalid filename."), 400)

    file_path = Path(Config.UPLOAD_FOLDER) / filename
    if not file_path.exists():
        return None, (jsonify(success=False, message="File not found."), 404)

    return file_path, None


@prediction_bp.post("/predict/image")
def predict_uploaded_image():
    """Run prediction on an uploaded image file."""
    file_path, error_response = _get_uploaded_file_path()
    if error_response is not None:
        return error_response

    # The AI service handles preprocessing and model inference.
    result = predict_image(str(file_path))
    if result is None:
        return jsonify(success=False, message="Image prediction failed."), 500

    return jsonify(
        success=True,
        prediction=result["prediction"],
        confidence=result["confidence"],
    )


@prediction_bp.post("/predict/video")
def predict_uploaded_video():
    """Run prediction on an uploaded video file."""
    file_path, error_response = _get_uploaded_file_path()
    if error_response is not None:
        return error_response

    # The AI service predicts sampled frames and averages their probabilities.
    result = predict_video(str(file_path))
    if result is None:
        return jsonify(success=False, message="Video prediction failed."), 500

    return jsonify(
        success=True,
        prediction=result["prediction"],
        confidence=result["confidence"],
    )
