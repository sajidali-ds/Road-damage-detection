import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MODEL_PATH, CLASS_NAMES


def test_model_file_exists():
    assert os.path.exists(MODEL_PATH), (
        f"Model file not found at {MODEL_PATH}. "
        "Download best_model.keras from Colab/Drive and place it in models/."
    )


def test_class_names_configured():
    assert len(CLASS_NAMES) == 7
    assert all(isinstance(name, str) and name for name in CLASS_NAMES)
