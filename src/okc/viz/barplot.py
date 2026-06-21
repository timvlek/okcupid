from matplotlib.axes import Axes
import pandas as pd
import numpy as np


def sorted_crosstab(
    index: pd.Series,
    columns: pd.Series,
    ascending: bool = True,
    **kwargs
) -> pd.DataFrame:
    
    """
    Generate a crosstab with ordered index and columns based on value counts.
    
    Parameters:
    - index (pd.Series): Values to group by rows.
    - columns (pd.Series): Values to group by columns.
    - ascending (bool): Order ascending if True (default: True).
    - kwargs: Additional arguments passed to pd.crosstab.
    
    Returns:
    - pd.DataFrame: Crosstab with ordered rows and columns.
    """
    
    ct = pd.crosstab(index, columns, **kwargs)
    index_order = index.value_counts(ascending=ascending).index
    column_order = columns.value_counts(ascending=True).index
    sorted_ct = ct[column_order].reindex(index_order)
    return sorted_ct


def barplot(
    df: pd.DataFrame,
    edgecolor = 'white', 
    grid: str | None = 'x',
    kind = 'barh',
    legend = None,
    stacked = True, 
    spines: list[str] = ['left'], 
    tick_params: dict[str, any] = dict(axis='both', which='both', length=0),
    xlabel: str = '',
    ylabel: str = '',
    xlim = None,
    **kwargs
) -> Axes:
    """
    Create a bar plot with customizable features using pandas plotting.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to plot.
    edgecolor : str, optional
        The color of the edges of the bars. Default is 'white'.
    grid : str | None, optional
        Whether to display gridlines ('x', 'y', 'both', or None). Default is 'x'.
    kind : str, optional
        The kind of plot to draw (e.g., 'bar', 'barh'). Default is 'barh'.
    legend : bool or None, optional
        Whether to include a legend. Default is None.
    stacked : bool, optional
        Whether to stack the bars. Default is True.
    spines : list[str], optional
        List of spines to display ('left', 'right', 'top', 'bottom'). Default is ['left'].
    tick_params : dict[str, any], optional
        Parameters for tick marks. Default is {'axis': 'both', 'which': 'both', 'length': 0}.
    xlabel : str, optional
        Label for the x-axis. Default is an empty string.
    ylabel : str, optional
        Label for the y-axis. Default is an empty string.
    xlim : tuple or None, optional
        Limits for the x-axis. Default is None.
    **kwargs : additional keyword arguments
        Additional keyword arguments
    """
   
    ax = df.plot(
        edgecolor=edgecolor, kind=kind, legend=legend, stacked=stacked, xlim=xlim, **kwargs
    )
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis=grid)
    ax.tick_params(**tick_params)

    for spine in spines:
        ax.spines[spine].set_visible(True)
    for spine in set(ax.spines.keys()) - set(spines):
        ax.spines[spine].set_visible(False)

    return ax


#  Define main function to run tests
def main():

    # Sample data generation
    np.random.seed(0)

    # Generate data
    parks = np.random.choice(['Park A', 'Park B', 'Park C'], size=100)
    species = np.random.choice(['Species X', 'Species Y', 'Species Z'], size=100)
    counts = np.random.randint(1, 20, size=100)

    # Create a DataFrame
    df = pd.DataFrame({
        'Park': parks,
        'Species': species,
        'Count': counts
    })

    # Test 1: generate a sorted crosstab
    ct = sorted_crosstab(index=df['Park'], columns=df['Species'], values=df['Count'], aggfunc='sum')
    print(ct)
    
    # Test 2: create a barplot
    barplot(df=ct, kind='barh', stacked=True, edgecolor='white', figsize=(10, len(ct)*5/7),
            legend=None, xlabel='', ylabel='', grid='x', spines=['left'], xlim=None
    )

    return

# Only run main if the script is executed (not imported)
if __name__ == "__main__":
    main()