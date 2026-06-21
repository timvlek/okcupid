from sklearn.pipeline import Pipeline
from sklearn.compose import TransformedTargetRegressor

def get_base_estimator_name(model) -> str:
    """
    Recursively extract the name of the underlying estimator.

    Parameters
    ----------
    model : object
        A scikit-learn estimator, possibly wrapped in pipelines or meta-estimators.

    Returns
    -------
    str
        The class name of the final underlying estimator.
    """

    while True:
        # Pipeline → take last step
        if isinstance(model, Pipeline):
            model = model.steps[-1][1]

        # TransformedTargetRegressor → unwrap regressor
        elif isinstance(model, TransformedTargetRegressor):
            model = model.regressor

        # GridSearchCV / RandomizedSearchCV
        elif hasattr(model, "best_estimator_"):
            model = model.best_estimator_

        # Generic fallback (some sklearn wrappers use .estimator)
        elif hasattr(model, "estimator"):
            model = model.estimator

        else:
            break

    return model.__class__.__name__