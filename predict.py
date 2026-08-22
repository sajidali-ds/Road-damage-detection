import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

from config import MODEL_PATH, CLASS_NAMES
from preprocessing.preprocess import preprocess_image

model = load_model(MODEL_PATH)


def predict_image(image: Image.Image) -> dict:
    """Run prediction and return the top class plus all class probabilities."""
    processed = preprocess_image(image)
    predictions = model.predict(processed, verbose=0)[0]
    predicted_index = int(np.argmax(predictions))
    confidence = float(predictions[predicted_index])

    all_probs = {name: float(prob) for name, prob in zip(CLASS_NAMES, predictions)}

    return {
        "class": CLASS_NAMES[predicted_index],
        "confidence": confidence,
        "all_probs": all_probs,
    }