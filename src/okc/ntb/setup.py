"""
notebook_setup.py

This module provides functions to set up a Jupyter notebook environment by changing the working
directory to the script's directory, loading a CSS stylesheet and other settings.

Functions
---------
change_working_directory() -> None
    Change the current working directory to the script's directory. Ensures this function can
    only be executed once.

load_css(path: str = './assets/css/Codeacademy.css') -> None
    Load and apply a CSS stylesheet.

load_settings() -> None
    Load and apply various settings for interactive shells, warnings, plotting backends, 
    and libraries such as pandas, matplotlib, and seaborn.

flattened(d): 
    Helper function to flatten a nested dictionary into a single-level dictionary.
Flatten a nested dictionary.

Example Usage
-------------
from setup import change_working_directory, load_css, load_settings

# Change the working directory
change_working_directory()

# Load the CSS stylesheet
load_css()

Load other settings
load_settings()
"""

from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display, HTML
from typing import Any
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import warnings
import yaml









  
    
