import sys
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MODEL_PATH, TEST_DIR, IMG_SIZE, BATCH_SIZE, BASE_DIR


def main():
    model = tf.keras.models.load_model(MODEL_PATH)

    test_ds = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR, image_size=IMG_SIZE, batch_size=BATCH_SIZE,
        label_mode="categorical", shuffle=False,
    )
    class_names = test_ds.class_names

    test_loss, test_acc = model.evaluate(test_ds)
    print("Test Accuracy:", test_acc)
    print("Test Loss:", test_loss)

    predictions = model.predict(test_ds, verbose=1)
    y_pred = np.argmax(predictions, axis=1)
    y_true = np.concatenate([y.numpy().argmax(axis=1) for _, y in test_ds])

    print(classification_report(y_true, y_pred, target_names=class_names))

    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(10, 8))
    ConfusionMatrixDisplay(cm, display_labels=class_names).plot(ax=ax, xticks_rotation=45)
    plt.tight_layout()

    output_path = os.path.join(BASE_DIR, "reports", "confusion_matrix.png")
    plt.savefig(output_path)
    print(f"Confusion matrix saved to: {output_path}")


if __name__ == "__main__":
    main()
