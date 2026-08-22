import numpy as np
from sklearn.utils.class_weight import compute_class_weight


def get_class_weights(train_ds) -> dict:
    labels = np.concatenate([y.numpy().argmax(axis=1) for _, y in train_ds])

    weights = compute_class_weight(
        class_weight="balanced",
        classes=np.unique(labels),
        y=labels,
    )
    return dict(enumerate(weights))