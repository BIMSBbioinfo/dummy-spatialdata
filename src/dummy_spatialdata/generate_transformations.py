from .utils import default_shape   
from typing import Optional
from spatialdata.transformations import (
    Affine,
    MapAxis,
    Scale,
    Sequence,
    Translation,
    BaseTransformation, 
    Identity
)

import numpy as np

def generate_transformations(
    trans: Optional[dict] = None
) -> list[BaseTransformation]:
    """Generate a list of transformations based on the specified input.

    Parameters
    ----------  
    trans : dict, optional
        A dictionary specifying the transformations to be applied and their parameters.
        Example: {'image_0': ['identity', 'translation', 'scale']} or {'image_0': ['affine']}

    Returns
    -------
    list[BaseTransformation]
        A list of transformation objects corresponding to the specified transformations in the input.
    
    Notes   
    -----
    Following transformation types are recognized:
    - 'identity': No transformation is applied.
    - 'mapAxis': Permutation of x and y dimensions.
    - 'translation': A translation transformation with a fixed translation vector (e.g., [10, 20]).
    - 'scale': A scaling transformation with fixed scale factors (e.g., [0.5, 0.5]).
    - 'affine': An affine transformation with a fixed transformation matrix.
    if multiple transformations are given, the resulting transformation will be a `Sequence` type.

    """

    if trans is None or {}:
        return None

    coord_system = list(trans.keys())[0]
    coord_content = list(trans.items())[0][1]

    # check transformations
    if "transformations" in coord_content:
        trans = coord_content['transformations']
    else:    
        ValueError('\'transformations\' field for {i} has to be defined!')

    alltrans = []
    for tr in trans:
        if tr == 'identity':
            tr = Identity()
        elif tr == 'mapAxis':
            tr = MapAxis({"x": "y", "y": "x"})
        elif tr == 'translation':
            tr = Translation([10, 20], axes = ('x', 'y'))
        elif tr == 'scale':
            tr = Scale([0.5, 0.5], axes = ('x', 'y'))
        elif tr == 'rotation':
            theta = np.deg2rad(15)
            c = np.cos(theta)
            s = np.sin(theta)
            tr = Affine(matrix = [
                    [c, -s, 0],
                    [s, c, 0],
                    [0, 0, 1],
                ], 
                input_axes=('x', 'y'), output_axes=('x', 'y'))
        elif tr == 'affine':
            tr = Affine(matrix = [
                    [0.5, 0.2, 0],
                    [0.1, 0.5, 0],
                    [0, 0, 1],
                ], 
                input_axes=('x', 'y'), output_axes=('x', 'y'))
        else:
            raise ValueError(f'Transformation type \'{tr}\' not recognized. Please choose from \'identity\', \'mapAxis\', \'translation\', \'scale\', or \'affine\'.')
        alltrans.append(tr)
    
    if(len(alltrans) > 1):
        alltrans = Sequence(alltrans)
    elif len(alltrans) == 1:
        alltrans = alltrans[0]
    else:
        pass

    return {coord_system: alltrans}
    
def get_shape(
    coordinate_systems: dict = {},
    coord_system: Optional[str] = None
) -> dict:
    
    # check if the transformations are empty, 
    # if so, return default
    if not coordinate_systems or coord_system is None:
        return(default_shape())
    
    if coord_system in coordinate_systems:
        coord_system = coordinate_systems[coord_system]
    else:
        raise ValueError(f'No coordinate system with name \'{str(coord_system)}\' was found.')
    
    if "shape" in coord_system:
        shape = coord_system['shape']
    else:
        shape = default_shape()

    return shape
        
def get_basetransformations(
    coordinate_systems: dict = {}
) -> dict:
    
    if not isinstance(coordinate_systems, dict):
        raise ValueError('Malformed coordinate system! e.g. \{\'global\': \{\'transformations\': [\'affine\'], \'shape\': \{\'x\': 2000, \'y\': 2000\}\}')

    # transformations
    coord_systems = {}
    for i in coordinate_systems.keys():
        # convert to base transformations
        coord_systems.update(
            generate_transformations({i: coordinate_systems[i]})
        )
    return coord_systems
    