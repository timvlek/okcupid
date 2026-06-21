import pandas as pd

def df_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get a short summary of the DataFrame's statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the short summary statistics.

    Raises
    ------
    ValueError
        If the input is not a pandas DataFrame or if the DataFrame is empty.
    """

    # Validate the input type.
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    # Validate the input DataFrame.
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    # Identify dictionary columns.
    dict_cols_list = [c for c in df.columns if any(isinstance(x, dict) for x in df[c])]

    # Create a DataFrame with summary statistics.
    stats_df = pd.DataFrame({
        'No. rows': [len(df)], 
        'No. columns': [len(df.columns)], 
        'No. duplicated rows': [df.drop(columns=dict_cols_list).duplicated().sum()],
        'No. missing values': [df.isna().sum().sum()]
    })
    
    # Return the summary statistics.
    return stats_df