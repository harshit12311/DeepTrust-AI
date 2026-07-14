from pathlib import Path

import numpy as np
import torch

try:
    from services.image_service import preprocess_image
    from services.video_service import preprocess_video
except ModuleNotFoundError:
    from backend.services.image_service import preprocess_image
    from backend.services.video_service import preprocess_video


MODEL_PATH = Path(__file__).resolve().parents[2] / "model" / "best_model.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _load_model():
    """Load the PyTorch model once when this module is imported."""
    try:
        model = torch.load(MODEL_PATH, map_location=DEVICE)

        if isinstance(model, dict) and "model" in model:
            model = model["model"]

        model.to(DEVICE)
        model.eval()
        return model
    except (FileNotFoundError, RuntimeError, AttributeError, TypeError) as error:
        print(f"Model loading error: {error}")
        return None


MODEL = _load_model()


def _frame_to_tensor(frame):
    """Convert a 224x224 RGB frame into a normalized PyTorch tensor."""
    tensor = torch.from_numpy(frame.astype(np.float32) / 255.0)
    tensor = tensor.permute(2, 0, 1).unsqueeze(0)
    return tensor.to(DEVICE)


def _confidence_from_output(output):
    """Convert model output into a Fake/Real prediction dictionary."""
    if output.shape[-1] == 1:
        fake_probability = torch.sigmoid(output).item()
    else:
        probabilities = torch.softmax(output, dim=1)
        fake_probability = probabilities[0][1].item()

    prediction = "Fake" if fake_probability >= 0.5 else "Real"
    confidence = fake_probability if prediction == "Fake" else 1.0 - fake_probability

    return {
        "prediction": prediction,
        "confidence": round(confidence * 100, 2),
    }


def _predict_frame(frame):
    """Run inference for a single preprocessed frame."""
    if MODEL is None:
        return None

    with torch.no_grad():
        tensor = _frame_to_tensor(frame)
        output = MODEL(tensor)

        if isinstance(output, (list, tuple)):
            output = output[0]

        return _confidence_from_output(output)


def predict_image(image_path):
    """Preprocess an image and return its deepfake prediction."""
    try:
        processed_image = preprocess_image(image_path)
        if processed_image is None:
            return None

        return _predict_frame(processed_image)
    except (RuntimeError, ValueError, TypeError) as error:
        print(f"Image prediction error: {error}")
        return None


def predict_video(video_path):
    """Preprocess sampled video frames and return an averaged prediction."""
    try:
        processed_frames = preprocess_video(video_path)
        if not processed_frames:
            return None

        predictions = []
        for frame in processed_frames:
            prediction = _predict_frame(frame)
            if prediction is not None:
                predictions.append(prediction)

        if not predictions:
            return None

        fake_scores = [
            prediction["confidence"]
            if prediction["prediction"] == "Fake"
            else 100 - prediction["confidence"]
            for prediction in predictions
        ]
        average_fake_score = sum(fake_scores) / len(fake_scores)

        final_prediction = "Fake" if average_fake_score >= 50 else "Real"
        final_confidence = (
            average_fake_score
            if final_prediction == "Fake"
            else 100 - average_fake_score
        )

        return {
            "prediction": final_prediction,
            "confidence": round(final_confidence, 2),
        }
    except (RuntimeError, ValueError, TypeError) as error:
        print(f"Video prediction error: {error}")
        return None
