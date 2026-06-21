import itertools
import numpy as np
import pandas as pd
import scipy.stats as stats
from typing import Any, Callable

def gof_tests(
    df: pd.DataFrame,
    tests: dict[str, [Callable, dict]] = {"Chi²": [stats.chisquare, dict()]}
) -> pd.DataFrame:
    """
    Perform goodness-of-fit tests on each column of the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be tested.
    tests : dict[str, [Callable, dict], optional
        A dictionary where keys are test names and values are lists containing
        the test function (from scipy.stats) and a dictionary of keyword arguments
        to pass to the test function. Default is {"Chi²": [stats.chisquare, dict()]}.

    Returns
    -------
    pd.DataFrame
        DataFrame with p-values for each feature against each test. Columns represent
        the test names, rows represent the features (DataFrame columns), and cell values
        are the corresponding p-values.
    """
    # Initialize an empty list to store the results
    results = []

    # Define the Cartesian product of the features and tests
    product = itertools.product(df.columns, tests.items())

    # Iterate over every feature and test combination
    for feature, (test_name, test_info) in product:
        series = df[feature].dropna()  # Drop missing values from the series
        
        function, kwargs = test_info  # Unpack the test function and keyword arguments
        
        # Only calculate goodness of fit for non-numeric data
        if not pd.api.types.is_numeric_dtype(series):
            observations = series.value_counts().sort_index()
            n_categories = len(observations)
            n_observations = len(series)
            expectations = np.full(n_categories, n_observations / n_categories)
            
            # Call the test function and extract the p-value
            _, pval, *_ = function(observations, expectations, **kwargs)
            
            # Append the results to the list
            results.append([feature, test_name, pval])

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results, columns=["Feature", "Test", "p-value"])

    # Pivot the DataFrame to have tests as columns and features as index
    results_pt = results_df.pivot_table(
        index="Feature", columns="Test", values="p-value"
    ).reset_index()

    # Return the results DataFrame
    return results_pt