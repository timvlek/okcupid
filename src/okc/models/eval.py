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


# import pandas as pd
# from sklearn.base import BaseEstimator
# from sklearn.metrics import (
#     mean_absolute_error, 
#     mean_squared_error, 
#     ndcg_score, 
#     r2_score,
# )
# # from scipy.stats import spearmanr, kendalltau
# from typing import Callable
# from .utils import get_base_estimator_name

# def rmse(y_true, y_pred): 
#     return mean_squared_error(y_true, y_pred) ** 0.5

# def ndgc(y_true, y_pred):
#     # Reshape to 2D for ndcg_score
#     y_true_2d = y_true.reshape(1, -1)
#     y_pred_2d = y_pred.reshape(1, -1)
#     return ndcg_score(y_true_2d, y_pred_2d)

# def kendall(y_true, y_pred):
#     return kendalltau(y_true, y_pred).correlation

# def spearman(y_true, y_pred):
#     return spearmanr(y_true, y_pred).correlation

# def evaluate_model(
#     model: BaseEstimator,
#     X_test: pd.DataFrame,
#     y_test: pd.Series,
#     name: str | None = None,
#     metrics: dict[str, Callable] | None = None,
# ) -> pd.DataFrame:
#     """
#     Evaluate a fitted model on test data and return performance metrics.

#     Parameters
#     ----------
#     model : BaseEstimator
#         A fitted scikit-learn compatible model implementing `.predict()`.
#     X_test : pd.DataFrame
#         Test feature matrix.
#     y_test : pd.Series
#         True target values corresponding to X_test.
#     name : str, optional
#         Name of the model. If None, the model's class name is used.
#     metrics : dict[str, Callable], optional
#         Dictionary of metric functions. Keys are metric names and values
#         are callables with signature (y_true, y_pred) -> float.
#         If None, defaults to MAE and RMSE.

#     Returns
#     -------
#     pd.DataFrame
#         A single-row DataFrame containing evaluation metrics.
#     """

#     # Set default metrics if none are provided.
#     if metrics is None:
#         metrics = {
#             "MAE": mean_absolute_error,
#             "RMSE": rmse, 
#             "R2": r2_score,
#             "NDCG": ndgc,
#             # "Kendall": kendall,
#             # "Spearman": spearman,
#         }

#     # Set default model name if none is provided.
#     if name is None:
#         name = get_base_estimator_name(model)

#     # Make predictions.
#     y_pred = model.predict(X_test)

#     # Ensure numpy arrays (safe for metrics like ndcg)
#     if isinstance(y_test, pd.Series):
#         y_true = y_test.to_numpy()
#     else:
#         y_true = y_test

#     # Compute metrics
#     results = pd.DataFrame([{
#         'Model': name,
#         **{
#             metric_name: metric_func(y_true, y_pred)
#             for metric_name, metric_func in metrics.items()
#         }, 
#     }])

#     # Return the results.
#     return results