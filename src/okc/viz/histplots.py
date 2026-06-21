import math
import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib.axes import Axes
from pandas.api.types import (
    is_bool_dtype, 
    is_categorical_dtype,
    is_float_dtype, 
    is_integer_dtype, 
    is_numeric_dtype, 
    is_object_dtype, 
)
from typing import (
    Any, 
    Literal, 
    TypeAlias, 
)

ColumnSelector: TypeAlias = str |list[str] | None
Mode: TypeAlias = Literal["x", "y", "include", "exclude"]

def _validate_selection(x, y, include, exclude):
    active = [v is not None for v in (x, y, include, exclude)]
    if sum(active) != 1:
        raise ValueError("Exactly one of x, y, include, exclude must be set.")
                         

def _resolve_columns(
    df: pd.DataFrame,
    *,
    x: str | list[str] | tuple | None = None, 
    y: str | list[str] | tuple | None = None, 
    include: str | list[str] | tuple | None = None, 
    exclude: str | list[str] | tuple | None = None, 
) -> tuple[list[str], Literal["x", "y", "include", "exclude"]]:
    """
    Resolve a set of DataFrame columns based on a single selection mode.

    Exactly one of `x`, `y`, `include`, or `exclude` must be provided.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame used for column resolution.
    x : str, optional
        Single column name to use as x-axis or feature selection.
    y : str, optional
        Single column name to use as y-axis or target selection.
    include : str or list of str, optional
        Dtype specification passed to `df.select_dtypes(include=...)`.
        Returns all matching columns.
    exclude : str or list of str, optional
        Dtype specification passed to `df.select_dtypes(exclude=...)`.
        Returns all matching columns.

    Returns
    -------
    tuple[list[str], str]
        A tuple containing:
        - list of resolved column names
        - the active mode used ("x", "y", "include", or "exclude")

    Raises
    ------
    ValueError
        If no arguments or multiple conflicting arguments are provided,
        or if resolution produces no columns.
    KeyError
        If any resolved column does not exist in the DataFrame.
    """

    # Map all possible inputs into a single dictionary for conflict detection.
    provided = {"x": x, "y": y, "include": include, "exclude": exclude}

    # Identify which arguments were actually supplied (non-None).
    active = [k for k, v in provided.items() if v is not None]

    # Validate that exactly one selection mode is active.
    if len(active) != 1:
        raise ValueError(
            "Exactly one of x, y, include, exclude must be provided. "
            f"Got: {active}"
        )
    
    mode: Mode = active[0]
    
    # # Dispatch table: maps mode → logic to resolve columns.
    # dispatch = {
    #     "x": lambda: x,
    #     "y": lambda: y,
    #     "include": lambda: df.select_dtypes(include=include).columns.tolist(),
    #     "exclude": lambda: df.select_dtypes(exclude=exclude).columns.tolist(),
    # }

    # # Determine active mode (guaranteed single element from earlier check).
    # mode = active[0]
    
    # # Resolve columns using the selected strategy.
    # cols = dispatch[mode]()

    if mode == "x":
        cols = x

    elif mode == "y":
        cols = y

    elif mode == "include":
        cols = df.select_dtypes(include=include).columns.tolist()

    elif mode == "exclude":
        cols = df.select_dtypes(exclude=exclude).columns.tolist()

    else:
        raise RuntimeError("Unreachable mode detected")
    

    # Force the result to be a list.
    if isinstance(cols, str):
        cols = [cols]

    # Validate that resolution produced a list of columns.
    if cols is None:
        raise ValueError(f"Column resolution failed for mode='{mode}'")

    # Validate that we have at least one column after resolution.
    if not cols:
        raise ValueError(
            f"No columns resolved for mode='{mode}'. "
            "Check inputs or dtype filters."
        )

    # Validate that all columns exist in the DataFrame.
    if mode in {"x", "y"}:
        missing = [c for c in cols if c not in df.columns]
        if missing:
            raise KeyError(f"Columns not in DataFrame: {missing}")

    return cols, mode

def _resolve_bins(series, n_bins):

    dtype = series.dtype

    if pd.api.types.is_bool_dtype(dtype):
        return 2

    elif pd.api.types.is_integer_dtype(dtype):
        return min(series.abs().max(), n_bins)

    elif pd.api.types.is_numeric_dtype(dtype):
        return n_bins
    
    elif (
           pd.api.types.is_categorical_dtype(dtype)
        # or pd.api.types.is_object_dtype(dtype)
        # or pd.api.types.is_string_dtype(dtype)
    ):
        n_cats = series.nunique(dropna=True)
        # ordered = series.cat.ordered
        if n_cats > n_bins:
            return None
        return n_cats
    
    else:
        raise ValueError(f"Unsupported dtype for histogram: {dtype}")

    return None


def histplots(
    df: pd.DataFrame, 
    *, 
    x: ColumnSelector = None,
    y: ColumnSelector = None,
    include: ColumnSelector = None,
    exclude: ColumnSelector = None,
    n_rows: int | None = None, 
    n_cols: int = 3, 
    n_bins: int = 30, 
    invert: bool = False, 
    **plt_kwargs: Any, 
) -> np.ndarray[Axes]:
    """
    Seaborn-style histogram grid.

    Returns
    -------
    Axes or np.ndarray[Axes]
    """

    cols, mode = _resolve_columns(
        df=df, x=x, y=y, 
        include=include, 
        exclude=exclude
    )

    n_plots = len(cols)
    n_cols = min(n_cols, n_plots)
    n_rows = n_rows or math.ceil(n_plots / n_cols)
    n_bins = n_bins or int(np.log2(len(df)) + 1) * 2

    base_w, base_h = plt.rcParams["figure.figsize"]
    figsize = (base_w, base_h * n_rows / n_cols)

    fig, axes = plt.subplots(
        nrows=n_rows, 
        ncols=n_cols, 
        figsize=figsize, 
        squeeze=False, 
    )

    # Flatten the axes array.
    axes = axes.ravel()

    # Loop through each column.
    for i, col in enumerate(cols):

        ax = axes[i]
        dtype = df[col].dtype
        bins = _resolve_bins(series=df[col], n_bins=n_bins)

        if bins is None:
            warnings.warn(f"Skipping non-numeric column: {col}")
            ax.set_visible(False)
            continue

        # Plot the histogram based on the mode.
        if mode == "x":
            sns.histplot(data=df, x=col, ax=ax, bins=bins, **plt_kwargs)
            ax.set_xlabel(col, visible=True)
            ax.set_xlim(0, None)
            if invert:
                ax.invert_xaxis()

        # Plot the histogram based on the mode.
        elif mode == "y":
            sns.histplot(data=df, y=col, ax=ax, bins=bins, **plt_kwargs)
            ax.set_ylabel(col, visible=True)
            ax.set_ylim(0, None)
            if invert:
                ax.invert_yaxis()

    # Hide unused axes.
    for ax in axes[n_plots:]:
        ax.axis("off")

    # Adjust layout to prevent overlap.
    plt.tight_layout()


    # if n_plots == 1:
    #     return axes[0]

    return axes