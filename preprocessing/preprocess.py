import numpy as np
from PIL import Image
from tensorflow.keras.applications.efficientnet import preprocess_input

from config import IMG_SIZE


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Convert a PIL image into the exact shape/format the model expects."""
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE)
    image = np.array(image, dtype=np.float32)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image
