import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image
from preprocessing.preprocess import preprocess_image


def test_preprocess_output_shape():
    # A tiny grayscale image, deliberately the "wrong" size/mode
    img = Image.new("L", (50, 80))
    processed = preprocess_image(img)
    assert processed.shape == (1, 224, 224, 3), f"Got shape {processed.shape}"


def test_preprocess_rgb_passthrough():
    img = Image.new("RGB", (500, 500), color=(120, 60, 30))
    processed = preprocess_image(img)
    assert processed.shape == (1, 224, 224, 3)
