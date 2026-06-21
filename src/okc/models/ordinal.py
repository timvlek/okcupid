import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin

class OrdinalModel(BaseEstimator, RegressorMixin):
    """A wrapper for regression models to handle ordinal classification tasks."""
    def __init__(self, model, classes):
        self.model = model
        self.classes = np.array(classes)

        # SAFE contiguous mapping
        self.encode_map = {v: i for i, v in enumerate(self.classes)}
        self.decode_map = {i: v for i, v in enumerate(self.classes)}

    def fit(self, X, y):
        y_encoded = np.array([self.encode_map[v] for v in y])
        self.model.fit(X, y_encoded)
        return self

    def predict(self, X):
        y_pred = self.model.predict(X).astype(int)
        return np.array([self.decode_map[i] for i in y_pred])