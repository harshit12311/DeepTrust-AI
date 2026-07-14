import cv2


def preprocess_image(image_path):
    """Read and preprocess an image for model inference."""
    try:
        image = cv2.imread(image_path)

        if image is None:
            return None

        # Standardize input size before applying denoising and color conversion.
        resized_image = cv2.resize(image, (224, 224))
        blurred_image = cv2.GaussianBlur(resized_image, (5, 5), 0)
        processed_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB)

        return processed_image
    except (cv2.error, OSError, TypeError) as e:
     print(f"Image preprocessing error: {e}")
     return None