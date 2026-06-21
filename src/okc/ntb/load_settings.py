from IPython.core.interactiveshell import InteractiveShell
from typing import Any
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yaml


def flattened(
        d: dict[str: Any], 
        parent_key: str = "", 
        seperator: str = "."
    ) -> dict[str: Any]:
    """
    Flattens a nested dictionary into a single-level dictionary.

    Parameters
    ----------
    d : dict[str, Any]
        The nested dictionary to be flattened.
    parent_key : str, optional
        The prefix for the flattened keys, by default "".
    seperator : str, optional
        The separator between keys in the flattened dictionary, by default ".".

    Returns
    -------
    dict[str, Any]
        The flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{seperator}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flattened(v, new_key, seperator=seperator).items())
        else:
            items.append((new_key, v))
    return dict(items)


def load_settings() -> None:
    """
    Load and apply various settings for interactive shells, warnings, plotting backends, and libraries such as pandas, matplotlib, and seaborn.

    The function performs the following:
    1. Sets the IPython shell to display all interactive outputs.
    2. Ignores all warnings.
    3. Switches the matplotlib backend to "inline" for Jupyter notebooks.
    4. Resets all pandas options to their default values.
    5. Resets all matplotlib rc parameters to their default values.
    6. Resets all seaborn options to their default values.
    7. Sets seaborn style to "white".
    8. Loads pandas and matplotlib configuration options from YAML files and applies them.
    9. Sets specific pandas display options.
    """
    
    # Set ast_node_interactivity
    InteractiveShell.ast_node_interactivity = "all"

    # Set filterwarnings to ignore
    warnings.filterwarnings("ignore")

    # Set matplotlib backend to inline
    plt.switch_backend("module://ipykernel.pylab.backend_inline")

    # Set all pandas options to their default values
    pd.reset_option("all")

    # Set all matplotlib rc options to their default values
    plt.rcdefaults()

    # Set all seaborn options to their default values
    sns.reset_defaults()

    # Set seaborn style
    sns.set_style("white")

    # Load matplotlib options
    plt.style.use('../cfg/mpl/default.mplstyle')
    
    # Set pandas option not set in yaml file
    pd.set_option("display.float_format", "{:,.2f}".format)