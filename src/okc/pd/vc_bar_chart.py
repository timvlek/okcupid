import pandas as pd
import pandas.io.formats.style as s

def vc_bar_chart(
        df: pd.DataFrame, 
        column: str, 
        color: str = '#D65F5F', 
        # color: str = '#57A6DC',
        order: list = None, 
        num_cats: int = 31
    ) -> s.Styler:
    """
    Displays the value counts of a categorical column in a DataFrame with a bar chart.

    Args:
        df: The DataFrame containing the data.
        column_name: The name of the categorical column.
        color: the color of the bars

    Returns:
        The styled DataFrame with the bar chart.
    """

    # Create a DataFrame of the value counts
    vc = df[column].value_counts()
    vc = pd.DataFrame({
        column: vc.index, 'No. observations': vc
    })

    if order:
        vc = vc.loc[order].iloc[:num_cats,:]

    # Style the DataFrame
    styler = (vc.style
        .format({'No. observations': '{:,.0f}'})
        .hide(axis='index')
        .bar(subset=['No. observations'], color=color)
    )

    # Return the result
    return styler

def vc_styler(
        df: pd.DataFrame, 
        color: str='#D65F5F'
    ) -> s.Styler:

    # Style the DataFrame
    styler = (df.style
        .format({'No. observations': '{:,.0f}'})
        .hide(axis='index')
        .bar(subset=['No. observations'], color=color)
    )

    # Return the result
    return styler