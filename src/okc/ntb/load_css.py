from IPython.display import display, HTML
import yaml

def load_css(path: str = "../cfg/css/Codeacademy.css") -> None:
    """
    Loads and applies a CSS stylesheet for display in environments like Jupyter Notebooks.

    Parameters
    ----------
    path : str, optional
        The path to the CSS stylesheet to load. Defaults to
        "../assets/css/Codeacademy.css".

    Returns
    -------
    None

    Raises
    -------
    FileNotFoundError
        If the specified CSS file is not found.

    Notes
    -----
    This function is designed for use in interactive environments
    like Jupyter Notebooks to enhance the visual appearance of the output.

    Examples
    -------
    >>> load_css()  # Load the default CSS file
    >>> load_css("../custom_styles.css")  # Load a custom CSS file
    """

    try:
        with open(path, "r") as file:
            css = file.read()
            display(HTML(f"<style>{css}</style>"))
    except FileNotFoundError:
        print(f"CSS file not found at {path}")

    

