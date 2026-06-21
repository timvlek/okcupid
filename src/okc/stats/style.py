import pandas as pd
from  matplotlib.colors import LinearSegmentedColormap, to_hex
from typing import Any

def hypothesis_test_number_formatting(x):
    try:
        return f'{x:.2f}'
    except Exception:
        return x
    
def hypothesis_test_cell_coloring(val, criterion=.05):
    try:
        # Apply the color if the condition is met
        return f'color: {"red" if val < criterion else ""};'
    except Exception as e:
        # Return an empty string if there is an error in evaluation
        return ''
    
def diverging_cell_coloring(val, minimum, maximum, cmap):
    """
    Colors a numeric value based on its normalized position within a specified range and colormap.

    Args:
        val: The numeric value to color.
        minimum: The minimum value in the range.
        maximum: The maximum value in the range.
        cmap: The colormap object to use.

    Returns:
        A string containing the HTML style for the color.
    """

    try:
       
        # Normalize negative values to the 0-.5 range
        if val < 0:
            normalized_val = -.5 * (val - minimum) / minimum

        # Normalize psotive values to the .5-1 range
        else:
            normalized_val = .5 + (.5 * val / maximum)

        # Get the color from the colormap
        color_tuple = cmap(normalized_val)

        # Convert the color tuple to a hexadecimal string
        html_color = to_hex(color_tuple)

        # Return the HTML style for the color
        return f'color: {html_color};'
    
    # Handle potential exceptions (e.g., division by zero)
    except Exception as e:
        return ''
 

def diverging_coloring(series: pd.Series, cmap=None):
    """
    Highlights numeric input strings using a diverging colormap. Whites go to 0, reds to negative, and greens to positive.

    Args:
        series: A pandas Series representing a column of the DataFrame.
        cmap: The name of the colormap to use (default: "RdGy").

    Returns:
        A pandas Series containing the HTML styles to apply to each element of the column.
    """
  
    if cmap is None:
        colors = ["red", "white", "green"]
        cmap = LinearSegmentedColormap.from_list(
            name='red-green',
            colors=colors, 
            N=256
        )

    # Define mimimum and maximum
    try: 
        minimum = series.min()
        maximum = series.max()
        return series.map(lambda x: diverging_cell_coloring(x, minimum, maximum, cmap))

    except Exception as e:
        return series.style

def color_cell2(
    val1: Any, 
    val2: Any = None, 
    color: str = "red", 
    condition: str = "< .05"
) -> str:
    """
    Apply conditional coloring to a cell based on the value of another cell.

    Parameters
    ----------
    val1 : Any
        The primary value to evaluate for conditional coloring.
    val2 : Any, optional
        The secondary value providing the comparison for the conditional check.
        If None, defaults to the value of val1.
    color : str, optional (default='red')
        The color to apply if the condition is met.
    condition : str, optional (default='< .05')
        The condition to evaluate for coloring, as a string containing a comparison operator
        and a threshold value (e.g., '< .05').

    Returns
    -------
    str
        A CSS style string to apply to the cell, or an empty string if no styling is needed.

    Example
    -------
    >>> color_cell(0.04)
    'color: red;'
    >>> color_cell(0.06)
    ''
    >>> color_cell(0.06, 0.04, color="blue", condition=">= .05")
    'color: blue;'
    """

    # If val2 is not provided, use val1 for the condition check
    if val2 is None:
        val2 = val1

    try:
        # Apply the color if the condition is met
        return f"color: {color if eval(f'{val2} {condition}') else ''};"
    except Exception as e:
        # Return an empty string if there is an error in evaluation
        return ""
    
# def color_col(
#     df: pd.DataFrame, 
#     color_dict: dict[str, str]:
#     color: str = "red", 
#     condition: str = "< 0.05"
# ) -> pd.DataFrame.style:
   
#     styles = []

#     for target_feature, base_feature in color_dict:
#         target_val = row[target_feature]
#         base_val = row[base_feature]
#         styles.append(color_cell(val_target, val_base))
#     return styles

    # styler = df.style.apply(apply_style, axis=1)
    # return styler
    
def color_df(
    df1: pd.DataFrame, 
    df2: pd.DataFrame = None,
    color: str = "red", 
    condition: str = "< 0.05"
) -> pd.DataFrame.style:
    """
    Apply conditional coloring to df1 based on the corresponding values in df2.

    Parameters
    ----------
    df1 : pd.DataFrame
        The DataFrame whose cells will be colored.
    df2 : pd.DataFrame, optional
        The DataFrame providing the values for the conditional check.
    color : str, optional (default='red')
        The color to apply if the condition is met.
    condition : str, optional (default='< 0.05')
        The condition to evaluate for coloring.

    Returns
    -------
    pd.io.formats.style.Styler
        The styled DataFrame with conditional coloring applied.
    """

    if df2 is None:
        df2 = df1

    # Apply the color_cell function
    styler = df1.style.apply(lambda row: [
        color_cell2(row[col], df2.at[row.name, col], color=color, condition=condition) for col in df1.columns
    ], axis=1)
    
    return styler
    
    # Create a DataFrame of styles
    # styles = pd.DataFrame(
    #     [[color_cell(df1.iloc[i, j], df2.iloc[i, j], color, condition) 
    #       for j in range(df2.shape[1])] 
    #      for i in range(df2.shape[0])],
    #     index=df1.index, columns=df1.columns
    # )

    # # Apply the styles
    # return df1.style.apply(lambda _: styles, axis=None)

    


# def color_conditional(
#     val: Any, 
#     criterion: float = 0.05, 
#     color: str = "red"
# ) -> str:
#     """
#     Applies conditional coloring to a value based on a given criterion.

#     Parameters
#     ----------
#     val : Any
#         The value to evaluate for conditional coloring.
#     criterion : float, optional
#         The threshold value below which the cell will be colored. Defaults to 0.05.
#     color : str, optional
#         The color to apply if the value is below the criterion. Defaults to "red".

#     Returns
#     -------
#     str
#         A CSS style string to apply to the cell, or an empty string if no styling is needed.
#     """

#     try:
#         return f"color: {color if float(val) < criterion else ''};"
#     except Exception as e:
#         return ""


def scientific_formatting(val: Any) -> Any:
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
        return f"{val:.2e}"
    except Exception as e:
        return val


def number_formatting(val: Any, max_digits: int = 4) -> str:
    """Formats a value according to its data type and magnitude.

    Parameters
    ----------
    val : Any
        The value to format.
    max_digits : int, optional
        The maximum number of digits before applying scientific notation.
        Defaults to 4.

    Returns
    -------
    str
        The formatted value.

    Notes
    -----
    - Handles numeric, string, object, and categorical data types.
    - Applies scientific notation for large numbers.
    - Returns the original value for non-numeric types.
    """

    if isinstance(val, float):
        try:
            no_digits = len(str(abs(int(val))))
            if no_digits > max_digits:
                return f"{val:.2e}"
            else:
                return f"{val:.2f}"
        finally:
            return val

    if isinstance(val, (str, object, pd.Categorical)):
        try:
            val = int(val)
            if len(str(abs(val))) > (max_digits):
                return f"{val:.2e}"
        finally:
            return val

    # if isinstance(val, float):
    #     if len(str(abs(int(val)))) > 2:
    #         return f"{val:.2e}"


def style_dataframe(df: pd.DataFrame, **kwargs) -> pd.DataFrame.style:
    """
    Applies conditional formatting and number formatting to a pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to style.

    color_threshold : float, optional (default=0.05)
        The threshold value below which numeric cells will be colored red.
        You can pass additional keyword arguments to the `conditional_coloring`
        function for more customization (refer to its docstring for details).

    Returns
    -------
    pandas.DataFrame.style
        A Styled DataFrame object with the applied formatting and coloring.

    Notes
    -----
    This function employs two helper functions: `conditional_coloring` and `number_formatting`. `conditional_coloring` Defines the logic for coloring cells based on arguments provided through `**kwargs`. These arguments can be used to adjust the threshold value, color choices, etc.`number_formatting` Formats numeric values based on the number of digits.

    The function applies conditional coloring using a lambda function and then formats all values using `number_formatting`. Additionally, it hides the index for a cleaner presentation.

    Examples
    -------
    >>> import pandas as pd
    >>> data = {"A": [1, 1000, 0.001], "B": [2.5, 0.123, 4.2e-4]}
    >>> df = pd.DataFrame(data)
    >>> styled_df = style_dataframe(df, color_threshold=0.01)  # Adjust threshold as needed
    >>> styled_df
    """

    return df.style.map(
        lambda val: conditional_coloring(val, **kwargs)
    ).format(number_formatting).hide(axis="index")
