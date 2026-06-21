import os

def import_all_sub_modules(
        excluded: list[str] = None
    ) -> None:
    """
    Import all sub-modules in the current package except those specified in the excluded list.

    This function dynamically imports all Python modules in the same directory as the calling script,
    excluding "__init__.py" and any modules specified in the `excluded` list. It then sets the
    __all__ variable of the package to control what is exported when using `from package import *`.

    Parameters
    ----------
    excluded : list[str, ...]
        A list of module names to exclude from importing and exporting.

    Returns
    -------
    None

    Notes
    -----
    This function has the following side effects:
    - Modifies the global namespace by importing modules.
    - Sets the global __all__ variable.

    Examples
    --------
    >>> import_all_sub_modules(["modules_to_exclude"])
    """
    
    # Initialize an empty list for excluded modules if not provided
    if excluded is None:
        excluded = []

    # Get the path of the current directory 
    dir = os.path.dirname(os.path.abspath(__file__))

    # Get the names of all the modules in the directory
    modules = [f[:-3] for f in os.listdir(dir) if f.endswith(".py") and f != "__init__.py"]

    # Dynamically import all modules
    for module in modules: 
        __import__(module)

    # Make `__all__` globally accessible
    global __all__

    # Define the allowed imports when using `from package import *`
    __all__ = [m for m in modules if m not in excluded]