from itertools import product
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def violinplots(
    df: pd.DataFrame,
    orient: str = 'h',
    legend: bool = False,
    cat_features: list = None,
    num_features: list = None,
    **vp_kwargs,
) -> None:
    """
    Creates violin plots for all pairwise combinations of categorical and numerical features.

    Args:
        df: The DataFrame containing the data.
        orient: The orientation of the plots ('h' for horizontal, 'v' for
            vertical). Defaults to 'h'.
        legend: Whether to include a legend (only applicable if hue is used). 
            Defaults to False.
        cat_features: Optional list of categorical features. If None, all   
            categorical features in the DataFrame will be used. Defaults to None.
        num_features: Optional list of numerical features. If None, all 
            numerical features in the DataFrame will be used. Defaults to None.
        **vp_kwargs: Additional keyword arguments to pass to the `violinplot` 
            method of seaborn.

    Returns:
        None
    """

    # Define categorical features (including boolean)
    if cat_features == None:
        cat_features = df.select_dtypes(include=['category', 'boolean']).columns

    # Define numerical features
    if num_features == None:
        num_features = df.select_dtypes(include=['number']).columns

    # Define the number of subplot rows and columns
    ncols = len(num_features)
    nrows = len(cat_features)

    # Define figure size
    height = plt.rcParams['figure.figsize'][1]
    width = plt.rcParams['figure.figsize'][0]
    new_height = min(nrows * height / 3, 20)
    new_width = min(ncols * width / 3, 30)
    figsize = (new_width, new_height)

    # Create figure
    fig, axes = plt.subplots(
        ncols=ncols,
        nrows=nrows,
        figsize=figsize,
        constrained_layout=True,
    )

    # Create the combinations of categorical and numerical features
    c_product = product(*[cat_features, num_features])

    # Iterate over combinations
    for i, (cat_feature, num_feature) in enumerate(c_product):
        row, col = divmod(i, ncols)
        ax = axes[row, col]
        # ax = axes[*divmod(i, ncols)]

        # Create the violinlot
        sns.violinplot(
            x=num_feature,
            y=cat_feature,
            hue=cat_feature,
            legend=legend,
            orient=orient,
            data=df,
            ax=ax,
            **vp_kwargs,
        )
        
        # Set title for each subplot
        ax.set_title(
            label=f'{num_feature}',
            loc="left",
            fontdict=dict(fontweight="normal", color="grey")
        )
        
    # Adjust spacing between subplots
    plt.tight_layout()