import sys
import os
import tensorflow as tf
from tensorflow import keras

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MODEL_PATH, FINE_TUNE_EPOCHS
from Training.train import build_datasets, get_callbacks
from Training.class_weights import get_class_weights


def main():
    model = keras.models.load_model(MODEL_PATH)

    # Find the EfficientNetB0 base model layer inside the functional model
    base_model = None
    for layer in model.layers:
        if "efficientnet" in layer.name.lower():
            base_model = layer
            break

    if base_model is None:
        raise ValueError("Could not find the EfficientNet base model layer inside the loaded model.")

    base_model.trainable = True
    for layer in base_model.layers[:-20]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    train_ds, val_ds, class_names = build_datasets()
    class_weights = get_class_weights(train_ds)

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=FINE_TUNE_EPOCHS,
        class_weight=class_weights,
        callbacks=get_callbacks(),
    )

    print(f"Fine-tuning complete. Updated model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
