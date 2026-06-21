import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from typing import Any


def dumbbellplot(
    *args,
    data: pd.DataFrame,
    x: str, 
    y1: str, 
    y2: str, 
    grid: str = 'y',
    s: int = 100,
    xlabel: str = '',
    ylabel: str = '',
    palette: sns.palettes._ColorPalette = sns.color_palette(),
    spines: list[str] = ['bottom'], 
    zorder: int = 3,
    marker: str = 'o',
    # figsize: tuple[int, int] = (10,6),
    tick_params: dict[str: Any] = dict(axis='both', length=0),
    **kwargs
) -> matplotlib.axes.Axes:
    """
        Creates a dumbbell plot from the provided DataFrame.
        
        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing the data to plot.
        x : str
            Column name for the x-axis (usually dates).
        y1 : str
            Column name for the estimated values.
        y2 : str
            Column name for the actual values.
        grid : str, optional
            Axis for the grid lines, by default 'y'.
        s : int, optional
            Marker size, by default 100.
        xlabel : str, optional
            Label for the x-axis, by default ''.
        ylabel : str, optional
            Label for the y-axis, by default ''.
        palette : sns.palettes._ColorPalette, optional
            Color palette, by default sns.color_palette().
        spines : list[str], optional
            Spines to show, by default ['bottom'].
        zorder : int, optional
            Z-order for markers, by default 3.
        marker : str, optional
            Marker style, by default 'o'.
        figsize : tuple[int, int], optional
            Figure size, by default (10, 6).
        tick_params : dict, optional
            Tick parameters, by default dict(axis='both', length=0).
        
        Returns
        -------
        matplotlib.axes.Axes
            The matplotlib Axes object containing the plot.
        """
   
    fig, ax = plt.subplots(*args, **kwargs)
    
    for i in range(len(data[x])):
        vline_color = palette[0] if data[y1][i] < data[y2][i] else palette[1]
        ymin=min(data[y2][i], data[y1][i])
        ymax=max(data[y2][i], data[y1][i])
        ax.vlines(x=data[x][i], ymin=ymin, ymax=ymax, color=vline_color, alpha=0.7)
        ax.scatter(data[x][i], data[y1][i], marker=marker, color=palette[1], s=s, zorder=zorder, **kwargs)
        ax.scatter(data[x][i], data[y2][i], marker=marker, color=palette[0], s=s, zorder=zorder, **kwargs)
   
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis=grid)
    ax.tick_params(**tick_params)
   
    for spine in spines:
        ax.spines[spine].set_visible(True)
    for spine in set(ax.spines.keys()) - set(spines):
        ax.spines[spine].set_visible(False)

    ax.scatter([], [], marker=marker, color=palette[0], label=y1)
    ax.scatter([], [], marker=marker, color=palette[1], label=y2)
    ax.legend(ncols=2, frameon=False)

    return ax


def main() -> matplotlib.axes.Axes:
    """
    Main function to create a DataFrame with test data and test function operation.
    
    Returns
    -------
    matplotlib.axes.Axes
        The matplotlib Axes object containing the plot.
    """
    # Example usage with sample data
    np.random.seed(0)
    dates = pd.date_range(start='2020-01-01', periods=8, freq='QE')
    eps_est = np.random.uniform(1, 3, len(dates))
    eps_act = eps_est + np.random.uniform(-0.5, 0.5, len(dates))

    data = pd.DataFrame({
        'date': dates,
        'eps_est': eps_est,
        'eps_act': eps_act
    })

    # Test the dumbbellplot function
    ax = dumbbellplot(data=data, x='date', y1='eps_est', y2='eps_act')
    ax.set_title('Netflix EPS Actuals Over Time')
    plt.show()
    return ax

if __name__ == "__main__":
    main()