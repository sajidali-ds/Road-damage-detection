from tensorflow import keras
from tensorflow.keras import layers


def get_data_augmentation() -> keras.Sequential:
    """Same augmentation pipeline used in the original Colab training notebook."""
    return keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.2),
        layers.RandomContrast(0.2),
    ])