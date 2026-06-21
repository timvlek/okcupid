# Import libraries
from matplotlib.axes import Axes
from matplotlib.colors import to_rgba
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Define a function to adjust colors to be slightly darker
def darken_color(color: str | tuple, amount: float = 0.3) -> tuple:
    """
    Adjust the given color to be slightly darker.

    Parameters:
    color (str or tuple): The color to be darkened, can be a hex string or an RGBA tuple.
    amount (float): The amount to darken the color by, default is 0.3.

    Returns:
    tuple: A tuple representing the darker color in RGBA format.
    """  

    # Convert the input color to RGBA format
    r, g, b, a = to_rgba(color)
    
    # Adjust the RGB components to be darker by the given amount
    r = r * (1 - amount)
    g = g * (1 - amount)
    b = b * (1 - amount)
    
    # Return the darker color as an RGBA tuple
    return r, g, b, a


# Define a custom boxplot function with type hints for parameters
def boxplot(
    *args, 
    figsize: tuple = (10,6),
    grid: str | None = 'x', 
    spines: list[str] = ['bottom'], 
    ticks: str| bool = 'both', 
    xlabel: str = '', 
    ylabel: str = '', 
    **kwargs
) -> Axes:
    """
    Custom boxplot function with type hints for parameters.

    Parameters:
    *args: Positional arguments passed to sns.boxplot().
    grid (Union[str, None]): Specifies the grid axis ('x', 'y', 'both') or None to disable grid.
    spines (List[str]): List of spines to show ('left', 'right', 'bottom', 'top').
    ticks (Union[str, bool]): Specifies the tick marks ('both', 'x', 'y') or False to disable ticks.
    xlabel (str): Label for the x-axis.
    ylabel (str): Label for the y-axis.
    **kwargs: Additional keyword arguments passed to sns.boxplot().

    Returns:
    Axes: The matplotlib Axes object containing the plot.
    """
    """
    Create a customized seaborn boxplot with additional styling options.

    Parameters:
    *args: Positional arguments passed to seaborn boxplot.
    **kwargs: Keyword arguments for customization.

    Returns:
    Axes object of the plot.
    """

    # Specific kwargs for additional customizations
    kwargs_list = ['figsize', 'grid', 'spines', 'ticks', 'xlabel', 'xlim', 'ylabel', 'ylim']
    custom_kwargs = {k: kwargs.pop(k) for k in kwargs_list if k in kwargs}

    # Extract data-related arguments
    data = kwargs.get('data')
    x = kwargs.get('x')
    y = kwargs.get('y')

    # Define the order of classes based on the median of the 'x' variable
    order = data.groupby(y)[x].median().sort_values(ascending=False).index

    # Set the figure size
    if 'figsize' in custom_kwargs:
        plt.figure(figsize=custom_kwargs.get('figsize'))
    
    # Create the seaborn boxplot
    ax = sns.boxplot(*args, order=order, **kwargs)

    # Apply customatizations
    for spine in spines:
        ax.spines[spine].set_visible(True)
    for spine in set(ax.spines.keys()) - set(spines):
        ax.spines[spine].set_visible(False)

    # Apply customatizations continued
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis=grid)
    ax.tick_params(axis=ticks, which='both', length=0)

    # Apply customatizations continued
    if 'xlim' in custom_kwargs:
        ax.set_xlim(custom_kwargs.get('xlim'))
    if 'ylim' in custom_kwargs:
        ax.set_ylim(custom_kwargs.get('ylim'))
    
    # Retrieve the palette used in the plot
    palette = [patch.get_facecolor() for patch in ax.patches]
    
    # Customize line colors
    for i, line in enumerate(ax.lines):
        color = palette[i // 6]
        darker_color = darken_color(color)
        line.set_markerfacecolor(color)
        line.set_markeredgecolor(darker_color)
        line.set_color(darker_color)

    return ax

# Define a decorater to customize seaborn boxplots
def customize_boxplot(boxplot_func):
    """
    Decorator to customize the appearance of seaborn boxplots.
    """
    
    def wrapper(
        *args, 
        grid: str | None = 'x', 
        spines: list[str] = ['bottom'], 
        ticks: str| bool = 'both', 
        xlabel: str = '', 
        ylabel: str = '', 
        **kwargs
    ) -> Axes:

        # Specific kwargs for additional customizations
        kwargs_list = ['figsize', 'xlim', 'ylim']
        custom_kwargs = {k: kwargs.pop(k) for k in kwargs_list if k in kwargs}

        # Extract data-related arguments
        data = kwargs.get('data')
        x = kwargs.get('x')
        y = kwargs.get('y')

        # Define the order of classes based on the median of the 'x' variable
        order = data.groupby(y)[x].median().sort_values(ascending=False).index

        # Set the figure size
        if 'figsize' in custom_kwargs:
            plt.figure(figsize=custom_kwargs.get('figsize'))
        
        #  Create the seaborn boxplot
        ax = sns.boxplot(*args, order=order, **kwargs)

        # Apply customatizations
        for spine in spines:
            ax.spines[spine].set_visible(True)
        for spine in set(ax.spines.keys()) - set(spines):
            ax.spines[spine].set_visible(False)

        # Apply customatizations continued
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(axis=grid)
        ax.tick_params(axis=ticks, which='both', length=0)

        # Apply customatizations continued
        if 'xlim' in custom_kwargs:
            ax.set_xlim(custom_kwargs.get('xlim'))
        if 'ylim' in custom_kwargs:
            ax.set_ylim(custom_kwargs.get('ylim'))

        # Retrieve the palette used in the plot
        palette = [patch.get_facecolor() for patch in ax.patches]

        # Customize line colors
        for i, line in enumerate(ax.lines):
            color = palette[i // 6]
            darker_color = darken_color(color)
            line.set_markerfacecolor(color)
            line.set_markeredgecolor(darker_color)
            line.set_color(darker_color)

        return ax

    return wrapper


#  Define main function to run tests
def main():
    df = pd.DataFrame({
        'Scientific name': [
            'Species_0', 'Species_1', 'Species_2', 'Species_3', 'Species_4', 'Species_5', 'Species_6', 'Species_7', 'Species_8', 'Species_9', 'Species_10', 'Species_11', 'Species_12', 'Species_13', 'Species_14', 'Species_15', 'Species_16', 'Species_17', 'Species_18', 'Species_19', 'Species_20', 'Species_21', 'Species_22', 'Species_23', 'Species_24', 'Species_25', 'Species_26', 'Species_27', 'Species_28', 'Species_29'
        ],
        'Park': [
            'Yellowstone', 'Yosemite', 'Bryce', 'Great Smoky Mountains', 'Yellowstone', 'Yosemite', 'Bryce', 'Great Smoky Mountains', 'Yellowstone', 'Yosemite', 'Bryce', 'Great Smoky Mountains', 'Yellowstone', 'Yosemite', 'Bryce', 'Great Smoky Mountains', 'Yellowstone', 'Yosemite', 'Bryce', 'Great Smoky Mountains', 'Yellowstone', 'Yosemite', 'Bryce', 'Great Smoky Mountains', 'Yellowstone', 'Yosemite', 'Bryce', 'Great Smoky Mountains', 'Yellowstone', 'Yosemite'
        ],
        'No. observations': [
            120, 95, 130, 80, 200, 70, 150, 65, 180, 90, 110, 85, 140, 75, 115, 105, 170, 125, 160, 145, 100, 85, 135, 90, 110, 140, 105, 95, 130, 100
        ],
        'Class': [
            'Mammal', 'Bird', 'Fish', 'Reptile', 'Amphibian', 'Nonvascular plant', 'Vascular plant', 'Mammal', 'Bird', 'Fish', 'Reptile', 'Amphibian', 'Nonvascular plant', 'Vascular plant', 'Mammal', 'Bird', 'Fish', 'Reptile', 'Amphibian', 'Nonvascular plant', 'Vascular plant', 'Mammal', 'Bird', 'Fish', 'Reptile', 'Amphibian', 'Nonvascular plant', 'Vascular plant', 'Mammal', 'Bird'
        ],
        'Species': [
            'Species_0', 'Species_1', 'Species_2', 'Species_3', 'Species_4', 'Species_5', 'Species_6', 'Species_7', 'Species_8', 'Species_9', 'Species_10', 'Species_11', 'Species_12', 'Species_13', 'Species_14', 'Species_15', 'Species_16', 'Species_17', 'Species_18', 'Species_19', 'Species_20', 'Species_21', 'Species_22', 'Species_23', 'Species_24', 'Species_25', 'Species_26', 'Species_27', 'Species_28', 'Species_29'
        ],
        'Conservation status': [
            'Not listed', 'Threatened', 'Endangered', 'Species of concern', 'In recovery', 'Not listed', 'Threatened', 'Endangered', 'Species of concern', 'In recovery', 'Not listed', 'Threatened', 'Endangered', 'Species of concern', 'In recovery', 'Not listed', 'Threatened', 'Endangered', 'Species of concern', 'In recovery', 'Not listed', 'Threatened', 'Endangered', 'Species of concern', 'In recovery', 'Not listed', 'Threatened', 'Endangered', 'Species of concern', 'In recovery'
        ]
    })

    palette = {
        'Mammal': '#FF4E11',
        'Bird': '#FAB733',
        'Fish': '#66A3FF',
        'Reptile': '#5280FA',
        'Amphibian': '#FF8E15',
        'Nonvascular plant': '#808080',
        'Vascular plant': '#A0A0A0'
    }

    # Test 1: Basic custom boxplot
    boxplot(data=df, x='No. observations', y='Class')
    plt.show()

    # Test 2: Custom boxplot with extensive arguments
    boxplot(
        data=df, x='No. observations', y='Class', hue='Class', width=.5, whis=.975, flierprops=dict(marker='o', markersize=5), grid='x', figsize=(10, 6), ticks='both', xlabel='', ylabel='', xlim=(51, 210), palette=palette
    )

    # Test 3: Decorated boxplot
    @customize_boxplot
    def custom_boxplot(*args, **kwargs):
        return sns.boxplot(*args, **kwargs)

    custom_boxplot(
        data=df, x='No. observations', y='Class', hue='Class', width=.5, whis=.975, flierprops=dict(marker='o', markersize=5), grid='x', figsize=(10, 6), spines=['bottom'], xlabel='', ylabel='', xlim=(51, 210), 
    )
    plt.show()

    return


# Only run main if the script is executed (not imported)
if __name__ == "__main__":
    main()