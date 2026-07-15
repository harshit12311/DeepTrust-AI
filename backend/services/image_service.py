import cv2


def preprocess_image(image_path):
    """
    Read an image and convert it to RGB.
    No resizing or preprocessing is done here.
    """

    image = cv2.imread(image_path)

    if image is None:
        return None

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image