import pandas as pd
from typing import Any
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

def load_pd(path="../cfg/pd/default.yaml") -> None:

    # Load pandas options
    with open(path, "r") as file:
        pd_options = yaml.safe_load(file)
        
    # Set pandas options
    for option, value in flattened(pd_options).items():
        pd.set_option(f"{option}", value)