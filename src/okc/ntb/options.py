"""
options.py
"""

from IPython.core.interactiveshell import InteractiveShell
from typing import Any
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yaml


def flattened(d: dict[str, Any], parent_key: str = '', sep: str = '.') -> dict[str, Any]:
    """
    Flatten a nested dictionary.

    Parameters
    ----------
    d : dict
        The dictionary to flatten.
    parent_key : str, optional (default='')
        The base key for the flattened dictionary.
    sep : str, optional (default='.')
        The separator between the base key and nested keys.

    Returns
    -------
    dict
        The flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flattened(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
  
    
def load_settings() -> None:
    """
    Load and apply various settings for interactive shells, warnings, plotting backends, 
    and libraries such as pandas, matplotlib, and seaborn.

    The function performs the following:
    1. Sets the IPython shell to display all interactive outputs.
    2. Ignores all warnings.
    3. Switches the matplotlib backend to 'inline' for Jupyter notebooks.
    4. Resets all pandas options to their default values.
    5. Resets all matplotlib rc parameters to their default values.
    6. Resets all seaborn options to their default values.
    7. Sets seaborn style to 'white'.
    8. Loads pandas and matplotlib configuration options from YAML files and applies them.
    9. Sets specific pandas display options.
    """
    
    # Set ast_node_interactivity
    InteractiveShell.ast_node_interactivity = 'all'

    # Set filterwarnings to ignore
    warnings.filterwarnings('ignore')

    # Set matplotlib backend to inline
    plt.switch_backend('module://ipykernel.pylab.backend_inline')

    # Set all pandas options to their default values
    pd.reset_option('all')

    # Set all matplotlib rc options to their default values
    plt.rcdefaults()

    # Set all seaborn options to their default values
    sns.reset_defaults()

    # Set seaborn style
    sns.set_style('white')

    # Load pandas options
    with open('../config/pandas.yaml', 'r') as file:
        pandas_options = yaml.safe_load(file)

    # Load matplotlib options
    with open('../config/matplotlib.yaml', 'r') as file:
        matplotlib_options = yaml.safe_load(file)

    # Set pandas options
    # for option, value in src.utils.flattened(pandas_options).items():
    for option, value in flattened(pandas_options).items():
        pd.set_option(f'{option}', value)

    # Load stats_style options
    with open('../config/statistics.yaml', 'r') as file:
        stats_style = yaml.safe_load(file)

    # Set pandas option not set in yaml file
    pd.set_option('display.float_format', '{:,.2f}'.format)

    # Set matplotlib rc options
    plt.style.use(flattened(matplotlib_options))
    

def main() -> None:
    """
    Main function to load and apply settings by calling the load_settings function.

    The function performs the following:
    1. Loads and applies configurations for IPython shell, warnings, plotting backends, 
       and libraries such as pandas, matplotlib, and seaborn.
    2. Ensures the settings are applied when the script is executed directly.
    """
    load_settings()

    
# Run the main function if the script is executed
if __name__ == "__main__":
    main()