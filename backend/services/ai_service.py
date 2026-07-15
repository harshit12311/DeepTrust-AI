from pathlib import Path

import numpy as np
import torch

from model.model import DeepfakeClassifier

from backend.services.image_service import preprocess_image
from backend.services.video_service import preprocess_video



PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "model" / "best_model.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMAGENET_MEAN = torch.tensor([0.485, 0.456, 0.406], device=DEVICE).view(1, 3, 1, 1)
IMAGENET_STD = torch.tensor([0.229, 0.224, 0.225], device=DEVICE).view(1, 3, 1, 1)


def _load_model():
    """Create the classifier and load the trained checkpoint once."""
    try:
        model = DeepfakeClassifier(freeze_blocks=5, dropout=0.4, backbone="b4")
        state = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=True)

        model.load_state_dict(state)
        model.to(DEVICE)
        model.eval()

        return model
    except (FileNotFoundError, KeyError, RuntimeError, TypeError) as error:
        print(f"AI model loading error: {error}")
        return None


MODEL = _load_model()


def _image_to_tensor(image):
    """Convert a 224x224 RGB NumPy image into a normalized tensor."""
    tensor = torch.from_numpy(image.astype(np.float32) / 255.0)
    tensor = tensor.permute(2, 0, 1).unsqueeze(0).to(DEVICE)
    return (tensor - IMAGENET_MEAN) / IMAGENET_STD


def _prediction_from_probability(fake_probability):
    """Format a fake probability as the API prediction response."""
    prediction = "Fake" if fake_probability >= 0.5 else "Real"
    confidence = fake_probability if prediction == "Fake" else 1.0 - fake_probability

    return {
        "prediction": prediction,
        "confidence": round(confidence * 100, 2),
    }


def _predict_processed_image(image):
    """Run inference on one preprocessed image or video frame."""
    if MODEL is None:
        return None

    with torch.no_grad():
        tensor = _image_to_tensor(image)
        logits = MODEL(tensor)
        print("Raw model output:", logits)

        # If the checkpoint already outputs probabilities,
        # don't apply sigmoid again.
        if logits.min() >= 0 and logits.max() <= 1:
            fake_probability = logits.item()
        else:
            fake_probability = torch.sigmoid(logits).item()

    return fake_probability


def predict_image(image_path):
    """Predict whether an uploaded image is fake or real."""
    try:
        processed_image = preprocess_image(image_path)
        if processed_image is None:
            return None

        fake_probability = _predict_processed_image(processed_image)
        if fake_probability is None:
            return None

        return _prediction_from_probability(fake_probability)
    except (RuntimeError, ValueError, TypeError) as error:
        print(f"Image AI prediction error: {error}")
        return None


def predict_video(video_path):
    """Predict a video by averaging fake probabilities across sampled frames."""
    try:
        processed_frames = preprocess_video(video_path)

        print("Frames extracted:", len(processed_frames) if processed_frames else 0)

        if not processed_frames:
            return None

        fake_probabilities = []

        for frame in processed_frames:

            fake_probability = _predict_processed_image(frame)

            if fake_probability is not None:
                print("Frame probability:", fake_probability)
                fake_probabilities.append(fake_probability)

        if not fake_probabilities:
            return None

        average_fake_probability = sum(fake_probabilities) / len(fake_probabilities)

        return _prediction_from_probability(average_fake_probability)

    except (RuntimeError, ValueError, TypeError) as error:
        print(f"Video AI prediction error: {error}")
        return None
