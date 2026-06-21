import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def countplots(
    df: pd.DataFrame,
    include: list[str] = ['category', 'boolean'],
    ncols: int = 3,
    **cp_kwargs
) -> None:
    """
    Plots countplots for each categorical feature in the given DataFrame.

    Args:
        df: The DataFrame containing the categorical features.
        include: A list of data types to consider as categorical.
        ncols: The number of columns in the subplot grid.
        cp_kwargs: Additional keyword arguments to pass to the 
            countplot function.

    Returns:
        None
    """

    cat_features = list(df.select_dtypes(include=include).columns)
    max_cats = max(len(df[col].unique()) for col in cat_features)
    nrows = math.ceil(len(cat_features) / ncols)

    # Adjust figure size based on the number of categories and subplots
    height = plt.rcParams['figure.figsize'][1]
    width = plt.rcParams['figure.figsize'][0]
    new_height = nrows * max_cats
    figsize = (width, new_height / ncols)

    # Create a figure with subplots
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    # Flatten the axes for easier iteration
    axes_flattened = axes.flatten()

    # Loop through each categorical column and create a countplot
    for i, col in enumerate(cat_features):
        
        # Create the countplot
        sns.countplot(
            data=df, 
            y=col, 
            order=df[col].value_counts().index, 
            ax=axes_flattened[i], 
            **cp_kwargs
        )
        # Set y axis label and title for each subplot
        axes_flattened[i].set_ylabel('')
        axes_flattened[i].set_title(
            label=f'{col}',
            loc="left",
            fontdict=dict(fontweight="normal", color="grey")
        )

    # Hide redundant subplots
    for i in range(len(axes_flattened) - len(cat_features)):
        axes[nrows - 1, -i - 1].set_visible(False)

    # Adjust spacing between subplots if necessary
    plt.tight_layout()