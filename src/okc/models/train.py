import pandas as pd

from sklearn.base import BaseEstimator
from sklearn.metrics._scorer import _BaseScorer
from sklearn.model_selection import BaseCrossValidator
from typing import Callable

from sklearn.base import clone
from sklearn.metrics import (
    make_scorer,
    mean_absolute_error,
    root_mean_squared_error,
    r2_score,
)
from sklearn.model_selection import cross_val_score
from .utils import get_base_estimator_name


def _ensure_scorer(
    score_fn: Callable, 
    greater_is_better: bool = True
) -> Callable:
    if isinstance(score_fn, _BaseScorer):
        return score_fn
    return make_scorer(
        score_func=score_fn,
        greater_is_better=greater_is_better
    )


def eval_model(
    model: BaseEstimator,
    X: pd.DataFrame,
    y: pd.Series,
    cv: BaseCrossValidator | None = None,
    metrics: dict[str, Callable] | None = None,
    name: str | None = None,
) -> pd.DataFrame:
    
    if metrics is None:
        metrics = {
            "MAE": mean_absolute_error,
            "RMSE": root_mean_squared_error,
            "R2": r2_score,
        }

    model = clone(model)

    if name is None:
        name = get_base_estimator_name(model)

    scores = {"Model": name}

    # -------------------------
    # NO CV MODE
    # -------------------------
    if cv is None:
        model.fit(X, y)
        y_pred = model.predict(X)

        scores.update({
            m: fn(y, y_pred)
            for m, fn in metrics.items()
        })


    # -------------------------
    # CV MODE
    # -------------------------
    for metric, fn in metrics.items():
        scorer = _ensure_scorer(fn)

        scores[metric] = float(
            cross_val_score(
                estimator=model,
                X=X,
                y=y,
                cv=cv,
                scoring=scorer,
            ).mean()
        )

    return pd.DataFrame([scores])
