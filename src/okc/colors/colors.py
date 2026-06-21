from matplotlib.colors import LinearSegmentedColormap, ListedColormap
# import deprecation
import seaborn as sns

from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import seaborn as sns

def create_cmaps(
    diverging_name: str = "RdYlBu", 
    qualitative_name: str = "tab20", 
    name: str = None, 
    N: int = 256, 
    n_colors: int = 20
) -> LinearSegmentedColormap:
    """
    Generate a collection of colormaps including sequential and diverging types.

    Parameters
    ----------
    diverging_name : str, optional
        Name of the diverging colormap to use, by default "RdYlBu".
    qualitative_name : str, optional
        Name of the qualitative colormap to use, by default "tab20".
    name : str, optional
        Base name for the generated colormaps. Not used internally.
    N : int, optional
        Number of colors in the colormap, by default 256.
    n_colors : int, optional
        Number of colors to sample from the qualitative palette, by default 20.

    Returns
    -------
    tuple
        A tuple containing five LinearSegmentedColormap objects:
        - Sequential black colormap
        - Sequential white colormap
        - Sequential two-tone colormap
        - Diverging black colormap
        - Diverging white colormap
    """
    vals = np.linspace(0, 1, n_colors)

    # Set the qualitative colormap as the active seaborn palette
    sns.set_palette(qualitative_name, n_colors=n_colors)

    # Create a qualitative palette
    qualitative_palette = sns.color_palette(qualitative_name, n_colors=n_colors)

    # Define the colors for a cyclic colormap
    colors = [sns.color_palette()[i] for i in [0,4,2,6,12,8,0]]

    # Assuming create_cyclic_cmap is defined elsewhere and imported as src.colors.create_cyclic_cmap
    # cyclic_cmap = src.colors.create_cyclic_cmap(colors=colors)

    # Define the primary colors for any sequential colormap
    color_one = sns.color_palette()[0]
    color_two = sns.color_palette()[6]

    # Sequential black cmap
    sequential_black_cmap = LinearSegmentedColormap.from_list(
        name="Sequential black cmap", colors=[color_one, (0, 0, 0)], N=N
    )

    # Sequential white cmap
    sequential_white_cmap = LinearSegmentedColormap.from_list(
        name="Sequential white cmap", colors=[color_one, (1, 1, 1)], N=N
    )

    # Sequential two-tone cmap
    sequential_two_tone_cmap = LinearSegmentedColormap.from_list(
        name="Sequential two-tone cmap", colors=[color_one, color_two], N=N
    )

    # Diverging black cmap
    diverging_black_cmap = LinearSegmentedColormap.from_list(
        name="Diverging black cmap", colors=[color_one, (0, 0, 0), color_two], N=N
    )

    # Diverging white cmap
    diverging_white_cmap = LinearSegmentedColormap.from_list(
        name="Diverging white cmap", colors=[color_one, (1, 1, 1), color_two], N=N
    )

    return (
        sequential_black_cmap,
        sequential_white_cmap,
        sequential_two_tone_cmap,
        diverging_black_cmap,
        diverging_white_cmap
    )

def create_cyclic_cmap(
    colors: list[str | tuple],
    name: str = None,
    N: int = 256
) -> LinearSegmentedColormap:
    """
    Create a cyclic colormap from a list of colors.

    Parameters
    ----------
    colors : list of str or list of tuple
        A list of colors specified as strings or RGB tuples.
    name : str, optional
        The name of the resulting colormap. Default is None.
    N : int, optional
        Number of RGB quantization levels. Default is 256.

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        The created cyclic colormap.
    """
    # Create the colormap using the provided colors
    cmap = LinearSegmentedColormap.from_list(name=name, colors=colors, N=N)    
    
    # Return the created colormap
    return cmap

# @deprecation.deprecated(details=
#     """
#     Functionality is obsolete. Use 
#     matplotlib.colors.LinearSegmentedColormap.from_list() directly
#     """
# )
# def concat_cmaps(
#     cmaps: list[LinearSegmentedColormap | ListedColormap],
#     name: str = None
# ) -> LinearSegmentedColormap:
#     """
#     Concatenate multiple colormaps into one.

#     Parameters
#     ----------
#     cmaps : list of LinearSegmentedColormap or ListedColormap
#         List of colormaps to concatenate.
#     name : str, optional
#         The name of the new concatenated colormap. Default is None.

#     Returns
#     -------
#     matplotlib.colors.LinearSegmentedColormap
#         A new concatenated colormap.
#     """
#     # Calculate the number of colors per input colormap
#     n_cmaps = len(cmaps)
#     vals = np.linspace(0, 1, 256//n_cmaps)
    
#     # Extract colors from each input colormap
#     colors = np.vstack([cmap(vals) for cmap in cmaps])
    
#     # Create a new colormap from the concatenated colors
#     cmap = LinearSegmentedColormap.from_list(name=name, colors=colors)
    
#     # Return the new concatenated colormap
#     return cmap

# @deprecation.deprecated(details=
#     """
#     Functionality is obsolete. Use 
#     matplotlib.colors.LinearSegmentedColormap.from_list() directly
#     """
# )
# def concat_palettes(
#     palettes: list[sns.palettes._ColorPalette]
# ) -> sns.palettes._ColorPalette:
#     """
#     Concatenate multiple color palettes into one.

#     Parameters
#     ----------
#     palettes : list of sns.palettes._ColorPalette
#         List of seaborn color palettes to concatenate.

#     Returns
#     -------
#     sns.palettes._ColorPalette
#         The concatenated color palette.
#     """
#     # Initialize an empty list to store the concatenated palette
#     concatenated_palette = []
   
#     # Iterate through each palette and add its colors to the concatenated palette
#     for palette in palettes:
#         concatenated_palette += palette
   
#     # Return the concatenated color palette
#     return sns.color_palette(concatenated_palette)

# @deprecation.deprecated(details=
#     """
#     Functionality is obsolete. Use 
#     matplotlib.colors.LinearSegmentedColormap.from_list() directly
#     """
# )
# def create_diverging_cmap(
#     left_cmap: LinearSegmentedColormap | ListedColormap,
#     right_cmap: LinearSegmentedColormap | ListedColormap,
#     name: str = None
# ) -> LinearSegmentedColormap:
#     """
#     Create a diverging colormap by combining two colormaps.

#     Parameters
#     ----------
#     left_cmap : LinearSegmentedColormap or ListedColormap
#         The left colormap.
#     right_cmap : LinearSegmentedColormap or ListedColormap
#         The right colormap.
#     name : str, optional
#         Name for the combined colormap. Default is None.

#     Returns
#     -------
#     matplotlib.colors.LinearSegmentedColormap
#         The combined diverging colormap.
#     """
#     # Resample the left colormap to 128 colors
#     left = left_cmap._resample(128)
   
#     # Resample the right colormap to 128 colors
#     right = right_cmap._resample(128)
   
#     # Combine the two colormaps into one
#     cmap = np.vstack((
#         left(np.linspace(0, 1, 128)),
#         right(np.linspace(0, 1, 128))
#     ))
    
#     # Create a new LinearSegmentedColormap from the combined colormap
#     return LinearSegmentedColormap.from_list(name=name, colors=cmap)