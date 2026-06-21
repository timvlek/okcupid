import pandas as pd

def custom_fmt(x: object) -> object:
    """
    Format numeric values for display.

    Small numbers are rounded to 2 decimal places.
    Medium numbers are rounded to 1 decimal place.
    Large numbers are formatted with thousand separators and no scientific notation.
    """

    # Exclude boolean and NaN values.
    if isinstance(x, bool) or pd.isna(x):
        return x

    if isinstance(x, (int, float)):

        # Compute absolute value to determine magnitude class.
        abs_x = abs(x)

        # Format very small numbers (< 10) with higher precision.
        if abs_x < 10:
            return f"{x:.2f}"

        # Format medium-sized numbers (< 100) with moderate precision.
        if abs_x < 100:
            return f"{x:.1f}"

        # Format large numbers with thousand separators and no decimals.
        return f"{x:,.0f}"

    # Return non-numeric values unchanged.
    return x