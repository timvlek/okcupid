import pandas as pd
from pandas.io.formats.style import Styler

def vc_table(
        df: pd.DataFrame, 
        column: str, 
        # color: str = '#D65F5F', 
        color: str = '#57A6DC',
        order: list = None, 
        n_cats: int = 31
    ) -> Styler:
    """
    Displays the value counts of a categorical column in a DataFrame with a bar chart.

    Args:
        df: The DataFrame containing the data.
        column_name: The name of the categorical column.
        color: the color of the bars.
        order: The order in which to display the categories.
        n_cats: The maximum number of categories to display.

    Returns:
        The styled DataFrame with the bar chart.
    """

    # Create a DataFrame of the value counts.
    vc = df[column].value_counts()
    vc = pd.DataFrame({
        column: vc.index,
        'No. observations': vc
    })

    if order:
        # vc = vc.loc[order].iloc[:n_cats,:]
        vc = vc.reindex(order)

    vc = vc.dropna().iloc[:n_cats]

    # Style the DataFrame.
    styler = (vc.style
        .format({'No. observations': '{:,.0f}'})
        .hide(axis='index')
        .bar(subset=['No. observations'], color=color)
    )

    # Return the result.
    return styler

# [col.rjust(padding) for col in flat_df.columns]