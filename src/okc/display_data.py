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
    }).style.hide(axis='index')

    return missing_df

def display_statistics(df, units=None):
    '''
    Display relevant statistics on all columns within a DataFrame.
    
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame with data to be analysed.
    
    Returns
    -------
    statistics_df : pandas.core.frame.DataFrame
        DataFrame with relevant statistics on all columns within the input data.
    '''

    import pandas as pd
    
    statistics_df = pd.DataFrame({
        'Feature': df.columns.tolist(),
        'Unit': [unit if unit else '' for unit in units] if units else ['' for unit in df.columns],
        'Type': df.dtypes, 
        'Count': [df[feature].count() for feature in df.columns],
        'Missing': [df[feature].isna().sum()/len(df) for feature in df.columns], 
        'Null': [df[feature].isnull().sum()/len(df) for feature in df.columns], 
        'Categories': [df[feature].nunique(dropna=True) if df[feature].dtype == 'object' else pd.NA for feature in df.columns], 
        'Mode': [str(df[feature].value_counts().idxmax()).split('.')[0] for feature in df.columns], 
        'Balance': [balance(df[feature]) if df[feature].dtype == 'object' else pd.NA for feature in df.columns], 
        'Min': [df[feature].min() if df[feature].dtype != 'object' else pd.NA for feature in df.columns], 
        'Mean': [df[feature].mean() if df[feature].dtype != 'object' else pd.NA for feature in df.columns], 
        'Median': [float(df[feature].median()) if df[feature].dtype != 'object' else pd.NA for feature in df.columns], 
        'Max': [df[feature].max() if df[feature].dtype != 'object' else pd.NA for feature in df.columns], 
        'SD': [df[feature].std() if df[feature].dtype != 'object' else pd.NA for feature in df.columns], 
        'MAD': [df[feature].mad() if df[feature].dtype != 'object' else pd.NA for feature in df.columns],
        'Skew': [df[feature].skew() if df[feature].dtype != 'object' else pd.NA for feature in df.columns], 
        'Kurtosis': [df[feature].kurt() if df[feature].dtype != 'object' else pd.NA for feature in df.columns]
    }).style.format({
        'Count':  '{:,.0f}', 
        'Missing': '{:,.0%}',
        'Null': '{:,.0%}',
        'Categories': '{:,.0f}',
        'Balance': '{:,.2f}' ,
        'Min': '{:,.0f}',
        'Mean': '{:,.1f}',
        'Median': '{:,.0f}', 
        'Max': '{:,.0f}',
        'SD': '{:,.1f}',
        'MAD': '{:,.1f}',
        'Skew': '{:,.2f}',
        'Kurtosis': '{:,.2f}'
    }).hide(axis='index')
    
    return statistics_df
    
def balance(seq):
    '''
    Calculate and return the Shannon entropy of series of nominal values.
    
    Parameters
    ----------
    seq : pandas.core.series.Series
        Data series to calculate the Shannon entropy of.
    
     Returns
    -------
    polynomial_df : pandas.core.frame.DataFrame
        DataFrame with columns log transformed.
    H/log(k) : float
        The Shannon entropy.
        The minimum value approaches 0 for extremely imbalanced groups. 
        The maximum value is 1 for completely balanced groups.
    '''
    
    from collections import Counter
    from numpy import log
    
    n = len(seq)
    classes = [(clas,float(count)) for clas,count in Counter(seq).items()]
    k = len(classes)
    
    H = -sum([ (count/n) * log((count/n)) for clas,count in classes]) # Shannon entropy
    return H/log(k)