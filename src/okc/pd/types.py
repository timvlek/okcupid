import pandas as pd

def is_ordinal_dtype(series: pd.Series) -> bool:
    if hasattr(series.dtype, 'ordered'):
        return series.dtype.ordered
    else: 
        return False
    
def is_nominal_dtype(series: pd.Series) -> bool:
    if hasattr(series.dtype, 'ordered'):
        return not series.dtype.ordered
    else: 
        return False

def is_binary_dtype(series: pd.Series) -> bool:
    if hasattr(series.dtype, 'categories'):
        return (True or False) in series.dtype.categories
    else:
        return False