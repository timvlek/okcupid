from pandas.api import types
import numpy as np
import pandas as pd


def column_statistics(df: pd.DataFrame, dropna=True) -> pd.DataFrame:
    """
    Generate summary statistics for all non-numerical columns in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to summarize.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing summary statistics for each non-numerical column:
        - dtype
        - number of unique values
        - most frequent value
        - frequency of most frequent value
        - number of missing values

    Raises
    ------
    ValueError
        If the input is not a pandas DataFrame or if the DataFrame is empty.
    """

    # Helper function to calculate the mode and its frequency.
    def _freq_mode(s: pd.Series, dropna=dropna) -> (str, int):
        """Helper function to calculate the mode and its frequency."""

        # Calculate the mode and its frequency, if the Series is not empty.
        if not s.empty:

            # Get the value counts of the Series.
            vc = s.value_counts(dropna=dropna)

            # Return the most common value and its count.
            return vc.index[0], vc.iloc[0]

        # Return 0, if the Series is empty.
        return pd.NA, 0
    
    # Helper function to validate the input DataFrame.
    def _validate_input(df:pd.DataFrame) -> pd.DataFrame:

        # Validate the input type.
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")

        # Validate the input DataFrame.
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

    # Validate the input.
    _validate_input(df)
    
    # Initialize an empty list.
    stats = []

    # Calculate the number of samples.
    n_samples = df.shape[0]

    # Iterate over columns.
    for col in df.columns:

        # Get the Series.
        s = df[col]

        # Calculate missing values.
        n_missing = s.isna().sum()

        # Calculate non-missing values.
        n_non_missing = s.notna().sum()

        # Calculate the frequency of missing values.
        freq_missing = n_missing / n_samples
     
        # Create summary statistics based on the data type.
        if types.is_numeric_dtype(s) :
            stats.append({
                'Feature': col,
                'Data type': s.dtype,
                'Mode': '-',
                'Frequency': '-',
                'Unique': s.nunique() == n_samples,
                'No. unique': '-',
                'No. missing': n_missing,
                'Missing': freq_missing,
                "Min": s.min(),
                'Median': s.median(),
                'Max': s.max(),
                'Mean': s.mean(),
                'SD': s.std(),
                'Variance': s.var(),
                'Skew': s.skew(),
                'Kurtosis': s.kurtosis(),
            })
        elif types.is_object_dtype(s):
            stats.append({
                'Feature': col,
                'Data type': s.dtype,
                'Mode': '-',
                'Frequency': '-',
                'Unique': '-',
                'No. unique': '-',
                'No. missing': n_missing,
                'Missing': freq_missing,
                "Min": '-',
                'Median': '-',
                'Max': '-',
                'Mean': '-',
                'SD': '-',
                'Variance': '-',
                'Skew': '-',
                'Kurtosis': '-',
            })
        elif (
            types.is_bool(s) 
            or types.is_categorical_dtype(s) 
            or types.is_string_dtype(s)
        ):
            mode, freq = _freq_mode(s)
            n_unique = s.nunique()
            stats.append({
                'Feature': col,
                'Data type': s.dtype,
                'Mode': mode, 
                'Frequency':freq, 
                'Unique': n_unique == n_samples,
                'No. unique': n_unique,
                'No. missing': n_missing,
                'Missing': freq_missing,
                "Min": '-',
                'Median': '-',
                'Max': '-',
                'Mean': '-',
                'SD': '-',
                'Variance': '-',
                'Skew': '-',
                'Kurtosis': '-',
            })
        else:
            stats.append({
                'Feature': col,
                'Data type': s.dtype,
                'Mode': '-',
                'Frequency': '-',
                'Unique': '-',
                'No. unique': '-',
                'No. missing': n_missing,
                'Missing': freq_missing,
                "Min": '-',
                'Median': '-',
                'Max': '-',
                'Mean': '-',
                'SD': '-',
                'Variance': '-',
                'Skew': '-',
                'Kurtosis': '-',
            })

    # Return the summary statistics as a DataFrame.
    return pd.DataFrame(stats)


# @singledispatch
# def stats_long(data: Any) -> list:
#     """
#     Base function for getting statistics from various types of data.
    
#     Parameters
#     ----------
#     data : any
#         The data to analyze.

#     Returns
#     -------
#     list
#         A list containing the statistics or placeholders for unsupported types.
    
#     Raises
#     ------
#     NotImplementedError
#         If the type of the data is not supported by any registered function.
#     """
#     raise NotImplementedError("Unsupported type")


# @stats_long.register
# def _(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Calculate descriptive statistics for each column in a DataFrame.

#     Parameters
#     ----------
#     data : pandas.DataFrame
#         DataFrame with data to be analyzed.

#     Returns
#     -------
#     pandas.DataFrame
#         DataFrame with descriptive statistics for each column in the input data.
#     """

#     num_columns = df.select_dtypes(include=['number']).columns
#     statistics_df = pd.DataFrame({
#         "Feature": df[num_columns].columns,
#         "Min": df[num_columns].min(),
#         "Median": df[num_columns].median(),
#         "Max": df[num_columns].max(),
#         "Mean": df[num_columns].mean(),
#         "SD": df[num_columns].std(),
#         "Variance": df[num_columns].var(),
#         "Skew": df[num_columns].skew(),
#         "Kurtosis": df[num_columns].kurtosis()
#     })

#     return statistics_df

def balance(data: pd.Series) -> float:
    """
    Calculate and return the balance of a Series of values 
    based on Shannon entropy.

    Parameters
    ----------
    data : pandas.Series
        Series to calculate the balance for.

    Returns
    -------
    float
        Balance measure based on Shannon entropy, normalized to [0, 1].
    """

    # Edge case if data is empty
    if data.empty:
        return np.nan

    # Calculate probabilities, entropy, and balance
    probs = data.value_counts(normalize=True)
    entropy = -sum(p * np.log2(p) for p in probs)
    balance = entropy / np.log2(len(probs))

    # Return the balance
    return balance


def main():
    """
    Main function to create a DataFrame with test data and compute statistics.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame containing statistics for the test data.
    """
    # Set np.random.seed for reproducibility
    np.random.seed(0)

    # Create a DataFrame with test data
    data = pd.DataFrame({
        "Integer": np.random.randint(100, 200, 100),
        "Float": np.random.np.random(100),
        "Boolean": np.random.choice([True, False], 100),
        "Category": np.random.choice(["A", "B", "C"], 100),
        "Datetime": pd.date_range(start="1/1/2020", periods=100),
        "Timedelta": [pd.Timedelta(days=i) for i in range(100)],
        "Text": np.random.choice(["foo", "bar", "baz"], 100),
        "Object": [f"object_{i}" for i in range(100)]
    })

    # Calculate statistics
    stats = stats_long(data)

    # Return statistics
    return stats

# Run the main function if the script is executed
if __name__ == "__main__":
    main()