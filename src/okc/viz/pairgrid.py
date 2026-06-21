import matplotlib as mpl
import seaborn as sns
import pandas as pd

def pairgrid(
        df: pd.DataFrame, 
        hue: str = None,
        palette: str | list[str] | dict[str: str] | mpl.colors.Colormap = sns.color_palette(),
        markers = ["o", "s", "v", "p", "h", "D", "X"],
        **kwargs
    ) -> sns.axisgrid.PairGrid:

    ax_args = kwargs.get('ax_args', {})
    pg_args = kwargs.get('pg_args', {})
    low_args = kwargs.get('low_args', {})
    diag_args = kwargs.get('diag_args', {})
    upper_args = kwargs.get('upper_args', {})

    if hue is not None:
        no_categories = df[hue].nunique()
        alpha = 1 / no_categories
        markers = markers[no_categories]

    g = sns.PairGrid(df, hue=hue, palette=palette, **pg_args)
    g.map_lower(sns.kdeplot, **low_args)
    g.map_diag(sns.kdeplot, **diag_args, fill=True)
    g.map_upper(sns.scatterplot, alpha=alpha, **upper_args)

    # if not ax_args.get("grid"):
    #     grid = False
    # if not ax_args.get("xticks"):
    #     xticks = []
    # if not ax_args.get("yticks"):
    #     yticks = []
    # if not ax_args.get("label_rotation"):
    #     label_rotation = 0
    # if not ax_args.get("labelpad"):
    #     labelpad = 60
    # if not ax_args.get("spines"):
    #     spines = ["bottom"]
    # for ax in g.axes.flat:
    #     ax.grid(grid)
    #     ax.set_xticks(xticks)
    #     ax.set_yticks(yticks)
    #     ax.yaxis.label.set_rotation(label_rotation)
    #     ax.yaxis.labelpad = labelpad

    #     for spine in spines:
    #         ax.spines[spine].set_visible(True)
    #     for spine in set(ax.spines.keys()) - set(spines):
    #         ax.spines[spine].set_visible(False)
    g.add_legend()
    # plt.subplots_adjust(top=0.9, wspace=0.1)
    # plt.suptitle('Distribution of features', size=16)
    return g