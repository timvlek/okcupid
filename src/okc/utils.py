def flattened(d, parent_key='', sep='.'):
    """
    Flatten a nested dictionary.

    Parameters:
    - d (dict): The dictionary to flatten.
    - parent_key (str): The key of the parent dictionary (used in recursion).
    - sep (str): The separator used between nested keys.

    Returns:
    - dict: A flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flattened(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_height()
        diff = current_width - new_value
        patch.set_height(new_value)
        patch.set_y(patch.get_y() + diff * .5)

def scale_column_values(df, columns=None, factors=None, copy=True, inplace=False):

    '''
    Scale column values of a dataframe to be of appropriate size for display.
    The lists of columns and scaling factors provided, should be of equal length.
    
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame with data to be analysed.
    columns: list
        List of column names, which values should be scaled.
    factors: list
        List of scaling factors. Values will be devided by the scaling factor.
    copy: bool, default True
        Also copy underlying data.
    inplace: bool, default False
        Whether to return a new DataFrame. If True then value of copy is ignored.
    
    Returns
    -------
    DataFrame or None
         DataFrame with all provided columns scaled or None if inplace=True.
    '''
    
    import pandas as pd
    
    if len(columns) != len(factors):
        return 'The lists of columns and scaling factors provided, should be of equal length.'
    
    if inplace==False:
        if copy==True:
            scaled_df = df.copy()
            for column, factor in zip(columns, factors):
                scaled_df[column]= scaled_df[column]/factor
            return scaled_df
        elif copy==False:
            for column, factor in zip(columns, factors):
                df[column]= df[column]/factor
            return df
    if inplace==True:
        for column, factor in zip(columns, factors):
            df[column]= df[column]/factor
        return

def display_missing_duplicates(df):
    '''
    Display statistics on missing and duplicate values within a DataFrame.
    
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame with data to be analysed.
    
    Returns
    -------
    missing_df : pandas.core.frame.DataFrame
        DataFrame with relevant statistics on all data.
    '''
    
    import pandas as pd
    
    missing_df = pd.DataFrame({
        'No. rows': [len(df)], 
        'No. columns': [len(df.columns)], 
        'No. duplicated values': [df.duplicated().sum()],
        'No. missing values': [df.isna().sum().sum()],
        'No. null values': [df.isnull().sum().sum()]
    })

    return missing_df