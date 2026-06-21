import itertools as it
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def pairplot(
    df: pd.DataFrame, 
    repeat: int = 2
):
    cat_cols = df.select_dtypes(exclude='number').columns
    num_cols = df.select_dtypes(include='number').columns

    # Define the number of subplot rows and columns
    ncols = len(df.columns)
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
        constrained_layout=True
    )

    # Create the appropriate plot
    for i, p in enumerate(it.product(df.columns, repeat=2)):
        x, y = p
        row, col = divmod(i, ncols)
        ax = axes[row, col]
        
        if x in num_cols and y in num_cols and x==y:
            sns.histplot(data=df, y=y, discrete=True, ax=ax)
        elif x in cat_cols and y in cat_cols and x==y:
            sns.histplot(data=df, y=x, discrete=True, ax=ax, hue=x, legend=False, alpha=.75)
        elif x in num_cols and y in num_cols:
            sns.scatterplot(data=df, x=x, y=y, alpha=.5, ax=ax)
        elif x in num_cols and y in cat_cols:
            sns.histplot(
                data=df, y=x, hue=y, discrete=True, multiple='stack',legend=False, ax=ax
            )
        elif x in cat_cols:
            sns.histplot(
                data=df, y=y, hue=x, discrete=True, multiple='stack', legend=False, ax=ax
            )
        else:
            pass

        # Set x-labels for the top row
        if row == 0:
            ax.xaxis.label.set_visible(True)
            ax.set_xlabel(y)
            ax.xaxis.set_label_position('top')
            # ax.xaxis.labelpad = 10 
        else:
            ax.set_xlabel('')
            ax.xaxis.set_label_position('top')
        
        # Set y-labels for the left column
        if col == 0:
            ax.set_ylabel(x)
        else:
            ax.set_ylabel('')

    plt.show()