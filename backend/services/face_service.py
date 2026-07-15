import cv2

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    
)
print("Cascade path:", cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
print("Cascade loaded:", not FACE_CASCADE.empty())

def extract_face(image):
    """
    Detect the largest face from an RGB image.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(60, 60),
    )

    if len(faces) == 0:
        return None

    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

    face = image[y:y+h, x:x+w]

    face = cv2.resize(face, (224, 224))

    return face