import pandas as pd

def duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Display statistics on missing and duplicate values within a DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with data to be analysed.
    
    Returns
    -------
    duplicates_df : pandas.DataFrame
        DataFrame with relevant statistics on all data.
    """

    duplicates_df = pd.DataFrame({
        'No. columns': [len(df.columns)],
        'No. rows': [len(df)], 
        'No. duplicated rows': [df.duplicated().sum()],
    })

    return duplicates_df