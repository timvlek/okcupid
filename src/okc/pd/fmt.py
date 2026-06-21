from typing import Any
import pandas as pd

def scientific(val: Any) -> Any:
    """
    Formats a numeric value in scientific notation with two decimal places.

    Parameters
    ----------
    val : Any
        The value to format.

    Returns
    -------
    str
        The formatted value in scientific notation, or the original value if formatting fails.
    """

    try:
        return f'{val:.2e}'
    except Exception as e:
        return val
    
stats = {
    'Min': '{:.0f}',
    'Median': '{:.0f}',
    'Max': '{:.0f}',
    'Missing': '{:.0%}',
    'Mean': '{:.2e}',
    'SD': '{:.2e}',
    'Variance': '{:.2e}',
    'Skew': '{:.2e}',
    'Kurtosis': '{:.2e}'
}

def ht_number(x):
    try:
        return f'{x:.2f}'
    except Exception:
        return x
    
def ht_color(x, criterion=.05):
    try:
        # Apply the color if the condition is met
        return f'color: {"red" if x < criterion else ""};'
    except Exception as e:
        # Return an empty string if there is an error in evaluation
        return ''
    
# def no_2(
#         series: pd.Series,
#         max_digits: int = 4
#     ) -> :
#     try:
#         no_digits = len(str(abs(int(max(series)))))
#         format = f'{:.2f}' if no_digits > max_digits else f'{max_digits:.2e}'
#         return series.style.format(format)
#     except Exception as e:
#         return series.style
        
# def no_1(series):
#     max_digits = len(str(abs(int(max(series)))))
#     formatter = f"{max_digits:.2f}" if max_digits > 4 else f"{max_digits:.2e}"
#     return series.map(lambda x: formatter.format(x))

