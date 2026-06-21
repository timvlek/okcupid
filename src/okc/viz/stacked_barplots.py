import matplotlib.pyplot as plt
import pandas as pd
from itertools import product

def stacked_barplots(
    df: pd.DataFrame,
    features: pd.Series = None,
    **p_kwargs,
) -> None:
    """
    Creates stacked bar plots for all pairwise combinations of categorical features.

    Args:
        df: The DataFrame containing the data.
        features: Optional list of categorical features. If None, all
            categorical features in the DataFrame will be used.
        p_kwargs: Additional keyword arguments to pass to the `plot` method
            of the crosstab.

    Returns:
        None
    """

    # Select categorical features (including boolean)
    if features is None:
        features = df.select_dtypes(include=['category', 'boolean'])

    # Define the number of subplot rows and columns
    ncols = len(features)
    nrows = ncols

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

    # Iterate over permutations
    for i, (feature_a, feature_b) in enumerate(product(features, repeat=2)):
        row, col = divmod(i, ncols)
        ax = axes[row, col]

        # Hide redundant plots efficiently
        if feature_a == feature_b:
            ax.set_visible(False)
            continue  
        
        # Create the cross-tabulation
        ct = pd.crosstab(
            index=df[feature_a],
            columns=df[feature_b],
        )

        # Label the rows and columns
        ct.columns = df[feature_a].unique()
        ct.index = df[feature_b].unique()

        # Plot the cross-tabulation
        ct.plot(kind='barh', stacked=True, ax=ax, **p_kwargs)

        # Set labels and title
        ax.set_ylabel(feature_b)
        ax.set_title(
            label=f'{feature_a}',
            loc="left",
            fontdict=dict(fontweight="normal", color="grey")
        )
    
    # Adjust spacing between subplots further
    plt.tight_layout()