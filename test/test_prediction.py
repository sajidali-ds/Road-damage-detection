import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image
from config import CLASS_NAMES
from predict import predict_image


def test_predict_returns_valid_class():
    dummy_image = Image.new("RGB", (300, 300), color=(128, 128, 128))
    result = predict_image(dummy_image)

    assert result["class"] in CLASS_NAMES
    assert 0.0 <= result["confidence"] <= 1.0
    assert set(result["all_probs"].keys()) == set(CLASS_NAMES)
    assert abs(sum(result["all_probs"].values()) - 1.0) < 1e-3