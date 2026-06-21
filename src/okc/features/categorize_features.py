import pandas as pd

def categorize_features(X: pd.DataFrame) -> list[list[str]]:
    """
    Categorizes features in the given DataFrame based on their data types:
    - Categorical features into nominal and ordinal
    - Boolean features
    - Numerical features

    Args:
    - X: pd.DataFrame
        The input DataFrame with various types of features (categorical, boolean, numerical).

    Returns:
    - list[list[str]]:
        A list containing four sublists:
        1. List of nominal categorical features
        2. List of ordinal categorical features
        3. List of boolean features
        4. List of numerical features
    """
    # Extract dtype metadata for categorical features.
    cat_dtypes = X.select_dtypes(include="category").dtypes

    # Identify boolean and numerical feature groups based on dtype.
    boo_cols = X.select_dtypes(include=["boolean"]).columns.tolist()
    num_cols = X.select_dtypes(include=["number"]).columns.tolist()

    # Split categorical features using the 'ordered' flag.
    nom_cols = cat_dtypes[~cat_dtypes.map(lambda dt: dt.ordered)].index.tolist()
    ord_cols = cat_dtypes[cat_dtypes.map(lambda dt: dt.ordered)].index.tolist()

    return [boo_cols, nom_cols, num_cols, ord_cols]