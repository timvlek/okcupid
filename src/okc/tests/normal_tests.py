import pandas as pd
import scipy.stats as stats
from typing import Callable

def normal_tests(
    df: pd.DataFrame,
    tests: dict[str, list[Callable, dict]] = {
        "Shapiro-Wilk": [stats.shapiro, dict()],
        "D'Agostino's K²": [stats.normaltest, dict()],
        "Kolmogorov-Smirnov": [stats.kstest, dict(cdf=stats.norm.cdf)],
        "Jarque-Bera": [stats.jarque_bera, dict()]
    }
) -> pd.DataFrame:
    """
    Perform various normality tests on each numeric column in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing the data to test.
    tests : Dict[str, List[Callable, Dict]], optional
        A dictionary specifying the normality tests to perform.
        Keys are test names, values are lists containing the test function
        and a dictionary of additional arguments. Default includes Shapiro-Wilk,
        D'Agostino's K², Kolmogorov-Smirnov, and Jarque-Bera tests.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the results of the normality tests for each numeric column.
        Rows represent different DataFrame columns, columns represent different tests.
        Each cell contains the p-value for the corresponding test and feature.

    Notes
    -----
    This function only tests numeric columns in the input DataFrame.
    Boolean columns and non-numeric columns are skipped.
    Some tests may not be applicable for small sample sizes or certain distributions.
    Errors during test execution are silently ignored.
    """
    # Initialize an empty list to store the results
    results = []

    # Iterate over each column in the DataFrame
    for col in df.columns:

        # Drop missing values from the series
        series = df[col].dropna()  

        try:
            # Iterate over each test defined in the `tests` dictionary
            for test, args in tests.items():

                # Unpack the test function and any additional keyword arguments
                function, kwargs = args

                # Call the test function and extract the p-value
                _, pval, *_ = function(series, **kwargs)

                # Append the results to the list
                results.append([col, test, pval])

        except Exception as e:
            pass

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results, columns=["Feature", "Test", "p-value"])

    # Pivot the DataFrame to have tests as columns and features as index
    results_pt = results_df.pivot_table(
        index="Feature", columns="Test", values="p-value"
    ).reset_index()

    # Return the results
    return results_pt