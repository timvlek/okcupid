from collections import Counter
from functools import singledispatch
from typing import Any
import numpy as np
import pandas as pd
import yaml


@singledispatch
def get_stats(data: Any) -> list:
    """
    Base function for getting statistics from various types of data.
    
    Parameters
    ----------
    data : any
        The data to analyze.

    Returns
    -------
    list
        A list containing the statistics or placeholders for unsupported types.
    
    Raises
    ------
    NotImplementedError
        If the type of the data is not supported by any registered function.
    """
    raise NotImplementedError("Unsupported type")


# @get_stats.register
# def _(data: pd.Series) -> pd.Series:
    # """
    # Calculate statistics for a Pandas Series.

    # Parameters
    # ----------
    # data : pandas.Series
    #     Series with data to be analyzed.

    # Returns
    # -------
    # pandas.Series
    #     Series of statistics calculated for the Series.
    # """

    # is_numeric = pd.api.types.is_numeric_dtype(data)
    # is_boolean = pd.api.types.is_bool_dtype(data)
    # is_datetime = pd.api.types.is_datetime64_any_dtype(data)
    # is_time_delta = pd.api.types.is_timedelta64_dtype(data)
    
    # # Handle numeric types excluding boolean
    # if (is_numeric and not is_boolean):

    #     # Calculate descriptive statistics
    #     stats = [
    #         data.min(),
    #         data.median(),
    #         data.max(),
    #         data.mean(),
    #         data.std(),
    #         data.var(),
    #         data.skew(),
    #         data.kurt()
    #     ]
    
    # # Handle datetime and timedelta types
     
    # elif (is_datetime or is_time_delta):

    #     # Calculate descriptive statistics
    #     stats = [
    #         data.min(),
    #         data.median(),
    #         data.max(),
    #         pd.NA,
    #         pd.NA,
    #         pd.NA,
    #         pd.NA,
    #         pd.NA,
    #     ]

    # # Default case for unsupported data types
    # else:
    #     # stats = 8 * [pd.NA]
    #     pass

    # # Return the list of descriptive statistics
    # return pd.Series(stats)



@get_stats.register
def _(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate descriptive statistics for each column in a DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame with data to be analyzed.

    Returns
    -------
    pandas.DataFrame
        DataFrame with descriptive statistics for each column in the input data.
    """

    num_columns = df.select_dtypes(include=['number']).columns
    statistics = pd.DataFrame({
        "Feature": df[num_columns].columns,
        "Min": df[num_columns].min(),
        "Median": df[num_columns].median(),
        "Max": df[num_columns].max(),
        "Mean": df[num_columns].mean(),
        "SD": df[num_columns].std(),
        "Variance": df[num_columns].var(),
        "Skew": df[num_columns].skew(),
        "Kurtosis": df[num_columns].kurtosis()
    })

                                
    # Initialize a dictionary to store descriptive statistics
    # results = pd.DataFrame(columns=[
    #     "Feature", "Min", "Median", "Max", "Mean", 
    #     "SD", "Variance", "Skew", "Kurtosis"
    # ])

    # # Define statistics to be calculated
    # names = [
    #     "Min", "Median", "Max", "Mean", 
    #     "SD", "Variance", "Skew", "Kurtosis"
    # ]

    # Compute statistics and add them to the dictionary
    # for col in df.columns:
    #     stat_values = get_stats(df[col])
    #     results = results.append([col]+get_stats(df[col]), ignore_index=True)

    # results = results.append([col]+stat_values, ignore_index=True)
        # for name, value in zip(names, values):
            # if stat not in stats:
            #     stats[stat] = pd.NA
            # results[stat].append(stat)

    # Return a DataFrame with the descriptive statistics
    return statistics

# def _(data: pd.DataFrame) -> pd.DataFrame:
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
#     # Initialize a dictionary to store descriptive statistics
#     stats = {
#         "Feature": data.columns.tolist(),
#         "Type": data.dtypes,
#         "Count": [data[col].count() for col in data.columns],
#         "No. categories": [data[col].nunique() for col in data.columns],
#         "No. missing": [data[col].isna().sum() for col in data.columns],
#         "Missing": [data[col].isna().mean() for col in data.columns],
#         "Mode": [data[col].mode().iloc[0] if not data[col].mode().empty else np.nan for col in data.columns],
#         # "Balance": [balance(data[col]) for col in data.columns]
#     }

#     # Define additional statistics to be calculated
#     stat_names = [
#         "Min", "Median", "Max", "Mean", 
#         "SD", "Variance", "Skew", "Kurtosis"
#     ]

#     # Compute additional statistics and add them to the dictionary
#     for col in data.columns:
#         additional_stats = get_stats(data[col])
#         for name, stat in zip(stat_names, additional_stats):
#             if name not in stats:
#                 stats[name] = []
#             stats[name].append(stat)

#     # Return a DataFrame with the descriptive statistics
#     return pd.DataFrame(stats)

def describe(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate descriptive statistics for each column in a DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame with data to be analyzed.

    Returns
    -------
    pandas.DataFrame
        DataFrame with descriptive statistics for each column in the input data.
    """
    # Initialize a dictionary to store descriptive statistics
    stats = {
        "Feature": data.columns.tolist(),
        "Type": data.dtypes,
        "Count": [data[col].count() for col in data.columns],
        "No. categories": [data[col].nunique() for col in data.columns],
        "No. missing": [data[col].isna().sum() for col in data.columns],
        "Missing": [data[col].isna().mean() for col in data.columns],
        "Mode": [data[col].mode().iloc[0] if not data[col].mode().empty else np.nan for col in data.columns],
        # "Balance": [balance(data[col]) for col in data.columns]
    }

    # Return a DataFrame with the descriptive statistics
    return pd.DataFrame(stats)

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
    stats = get_stats(data)

    # Return statistics
    return stats

# Run the main function if the script is executed
if __name__ == "__main__":
    main()