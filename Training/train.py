import sys
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE, EPOCHS, MODEL_PATH
from Training.class_weights import get_class_weights
from preprocessing.transform import get_data_augmentation


def build_datasets():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        TRAIN_DIR, image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode="categorical"
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        VAL_DIR, image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode="categorical"
    )

    class_names = train_ds.class_names
    print("Class order (matches label indices):", class_names)

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(autotune)
    val_ds = val_ds.prefetch(autotune)

    return train_ds, val_ds, class_names


def build_model(num_classes: int) -> keras.Model:
    data_augmentation = get_data_augmentation()

    base_model = EfficientNetB0(
        include_top=False, weights="imagenet", input_shape=(*IMG_SIZE, 3)
    )
    base_model.trainable = False  # frozen for initial training

    inputs = keras.Input(shape=(*IMG_SIZE, 3))
    x = data_augmentation(inputs)
    x = keras.applications.efficientnet.preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    return keras.Model(inputs, outputs)


def get_callbacks():
    return [
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True, verbose=1),
        keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=2, verbose=1),
        keras.callbacks.ModelCheckpoint(MODEL_PATH, monitor="val_accuracy", save_best_only=True, verbose=1),
    ]


def main():
    train_ds, val_ds, class_names = build_datasets()
    class_weights = get_class_weights(train_ds)
    print("Class weights:", class_weights)

    model = build_model(num_classes=len(class_names))
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.summary()

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        class_weight=class_weights,
        callbacks=get_callbacks(),
    )

    print(f"Training complete. Best model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
