import pandas as pd

class Formatter:
    """
    A class that encapsulates various formatting options for numeric values.
    This includes formatting in scientific notation, fixed-point float notation,
    and applying color highlighting based on a criterion.

    Methods
    -------
    scientific(x: object, n_decimals: int = 2) -> object
        Formats a numeric value in scientific notation with a customizable number of decimal places.
    float(x: object, n_decimals: int = 2) -> object
        Formats a numeric value to a fixed-point notation with a customizable number of decimal places.
    highlight(x: object, criterion: float = 0.05, color: str = "red") -> str
        Applies a color style if the value is less than a given criterion.
    custom(x: object) -> object
        Formats numeric values based on size: 
        - Small numbers (< 10) are rounded to 2 decimal places.
        - Medium numbers (< 100) are rounded to 1 decimal place.
        - Large numbers are formatted with thousand separators and no decimals.
    """

    @staticmethod
    def scientific(x: object, n_decimals: int = 2) -> object:
        """
        Formats a numeric value in scientific notation with a customizable number of decimal places.

        Parameters
        ----------
        x : object
            The value to format. Should be numeric.
        n_decimals : int, optional, default=2
            The number of decimal places to include in the scientific notation.

        Returns
        -------
        str or object
            The formatted value in scientific notation, or the original value if formatting fails.
        """
        if isinstance(x, (int, float)):
            return f'{x:.{n_decimals}e}'
        return x

    @staticmethod
    def float(x: object, n_decimals: int = 2) -> object:
        """
        Formats a numeric value to a fixed-point notation with a customizable number of decimal places.

        Parameters
        ----------
        x : object
            The value to format. Should be numeric.
        n_decimals : int, optional, default=2
            The number of decimal places to include in the float formatting.

        Returns
        -------
        str or object
            The formatted value with the specified number of decimal places, or the original value if formatting fails.
        """
        if isinstance(x, (int, float)):
            return f'{x:.{n_decimals}f}'
        return x

    @staticmethod
    def highlight(x: object, criterion: float = 0.05, color: str = "red") -> str:
        """
        Applies a color style if the value is less than a given criterion.

        Parameters
        ----------
        x : object
            The value to evaluate. Should be numeric.
        criterion : float, optional, default=0.05
            The threshold value to compare against.
        color : str, optional, default="red"
            The color to apply if the condition is met.

        Returns
        -------
        str
            A CSS-style string with the applied color if the condition is met, otherwise an empty string.
        """
        if isinstance(x, (int, float)) and x < criterion:
            return f'color: {color};'
        return ''
    
    @staticmethod
    def custom(x: object) -> object:
        """
        Formats numeric values for display based on their magnitude.

        - Small numbers (< 10) are rounded to 2 decimal places.
        - Medium numbers (< 100) are rounded to 1 decimal place.
        - Large numbers are formatted with thousand separators and no scientific notation.

        Parameters
        ----------
        x : object
            The value to format. Should be numeric.

        Returns
        -------
        str or object
            The formatted value based on size, or the original value if formatting fails.
        """

        # Exclude boolean and NaN values.
        if pd.isna(x):
            return x
        
        if isinstance(x, bool):
            return x
        
        if isinstance(x, int):
            return f"{x:,.0f}"

        if isinstance(x, float):

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