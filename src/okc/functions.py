import .Data.define_units

from pandas import crosstab
from scipy.stats import chi2_contingency
from numpy import sqrt

def cramers_v(x, y):
    '''
    Calculate Cramér's V.
    
    Cramér's V is a measure of association between two nominal variables, 
    giving a value between 0 and +1 (inclusive). 
    It is based on Pearson's chi-squared statistic.

    Parameters
    ----------
    x : pandas.core.series.Series
        Series of the first nominal variable.
    y : pandas.core.series.Series
        Series of the second nominal variable.
    
    Returns
    -------
    cramers_v : float
        Cramér's V is a measure of association between two nominal variables, 
        giving a value between 0 and +1 (inclusive). 
        It is based on Pearson's chi-squared statistic.
    '''

    cross_table = crosstab(x, y)
    X2 =chi2_contingency(cross_table)[0]
    n = cross_table.sum().sum()
    minDim = min(cross_table.shape)-1
    cramers_v = sqrt((X2/n) / minDim)
    
    return cramers_v