def load_config():
    
    # Import libraries.
    import itertools
    import math
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import missingno as msno
    import pandas as pd
    import numpy as np
    import nbextensions
    import seaborn as sns
    import scipy.stats as sps
    import warnings

    from IPython.core.interactiveshell import InteractiveShell
    from IPython.display import Latex
    from IPython.display import HTML
    from IPython.display import Image
    from IPython.display import Markdown as md
    from IPython.utils import io

    # Set CSS stylesheet
    HTML(open("Codecademy.css", "r").read())

    # Set ast_node_interactivity
    InteractiveShell.ast_node_interactivity = "all"

    # Set IPython notebook default options.
    # https://ipython.org/ipython-doc/2/config/options/notebook.html

    # Set warnings default options.
    # warnings.filterwarnings('ignore')  # Disable the display of warnings.

    # Define color palettes
    global single_hue_palette
    global color_palette
    global diverging_palette
    color_palette = ["#1d2340","#0000ff","#9d02d7","#cd34b5","#ea5f94","#fa8775","#ffb14e","#ffd700"]
    single_hue_palette = ['#003f5c', '#21526f', '#396582', '#507a96', '#668eaa', '#7ca4bf', '#93bad4', '#aad0e9', '#c2e7ff'][::-1]
    diverging_palette = ['#003f5c', '#365973', '#5b758b', '#8093a3', '#a4b1bd', '#cad0d6', '#f1f1f1', '#ead6e0', '#e2bcd0', '#daa2bf', '#d187af', '#c76da0', '#bc5090']

    # Set pandas default options.
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
    pd.options.display.date_yearfirst = True  # When True, prints and parses dates with the year first, eg 2005/01/20.
    pd.options.display.expand_frame_repr = False  # Whether to print out the full DataFrame repr for wide DataFrames across multiple lines, max_columns is still respected, but the output will wrap-around across multiple “pages” if its width exceeds display.width.
    pd.options.display.float_format = '{:,.0f}'.format  # The callable should accept a floating point number and return a string with the desired format of the number.
    pd.options.display.latex.multicolumn = True  # Combines columns when using a MultiIndex.
    pd.options.display.max_rows = None  # This sets the maximum number of rows pandas should output when printing out various output.
    pd.options.display.max_columns = None  # This sets the maximum number of columns pandas should output when printing out various output.
    # pd.options.display.max_colwidth = 10  # The maximum width in characters of a column in the repr of a pandas data structure.
    pd.options.display.multi_sparse = True  # “Sparsify” MultiIndex display (don’t display repeated elements in outer levels within groups.
    pd.options.display.precision = 2  # Floating point output precision in terms of number of places after the decimal.
    pd.options.display.width = None  # Width of the display in characters.
    pd.options.mode.chained_assignment = 'raise'  # Raise a SettingWithCopyException in case of chained assignment.
    pd.options.mode.use_inf_as_na = True  # Read (negative) infinity as NA.
    # pd.io.formats.style.Styler.render.sparse_index = True # “Sparsify” MultiIndex display for rows in Styler output (don’t display repeated elements in outer levels within groups).
    # pd.io.formats.style.Styler.render.sparse_columns = True # “Sparsify” MultiIndex display for columns in Styler output.
    # pd.set_eng_float_format(accuracy=2, use_eng_prefix=True) # to alter the floating-point formatting of pandas objects to produce a particular format in the console.
    # Don't wrap repr(DataFrame) across additional lines

    # Set matplotlib defaults
    # https://matplotlib.org/stable/tutorials/introductory/customizing.html
    # mpl.rc_file_defaults()
    plt.rcParams['grid.alpha'] = 1 # Set grid transparency, between 0.0 and 1.0
    plt.rcParams['figure.facecolor'] = 'white'  # Set figure face color.
    plt.rcParams['figure.figsize'] = (8, 5)  # Set figure size in inches.
    plt.rcParams['figure.titlesize'] = 10 # Set size of the figure title (``Figure.suptitle()``)
    plt.rcParams['figure.titleweight'] = 'bold'  # Set figure title font weight
    plt.rcParams['axes.facecolor'] = 'white'  # Set axes face color.
    plt.rcParams['axes.grid'] = True # Set display grid on or off
    plt.rcParams['axes.grid.axis'] = 'y' # Set axis which the grid should apply to
    plt.rcParams['axes.labelpad'] = 10  # Set space between label and axis.
    plt.rcParams['axes.labelsize'] = 10 # Set font size of the x and y labels
    plt.rcParams['axes.labelweight'] = 'normal'  # Set axis label font weight
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.spines.right'] = False # Set right spine on or off
    plt.rcParams['axes.spines.top'] = False # Set top spine on or off
    plt.rcParams['axes.titlelocation'] = 'left' # Set axes title location
    plt.rcParams['axes.titlepad'] = 15  # Set pad between axes and title in points.
    plt.rcParams['axes.titlesize'] = 15 # Set font size of the axes title
    plt.rcParams['axes.titleweight'] = 'normal' # Set figure title font weight
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['legend.title_fontsize'] = 10
    plt.rcParams['xaxis.labellocation'] = 'left'  # Set x-axis label location
    plt.rcParams['yaxis.labellocation'] = 'bottom'  # Set y-axis label location

    # Set seaborn defaults
    sns.set_context('notebook')
    sns.set_style('whitegrid')
    sns.set_palette(color_palette)
    
    return