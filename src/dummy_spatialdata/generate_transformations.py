from .utils import default_shape   
from typing import Optional
from spatialdata.transformations import (
    Affine,
    Scale,
    Sequence,
    Translation,
    BaseTransformation, 
    Identity
)

def generate_transformations(
    trans: Optional[dict] = None
) -> list[BaseTransformation]:
    """Generate a list of transformations based on the specified input.
    Parameters
    ----------  
    trans : dict, optional
        A dictionary specifying the transformations to be applied and their parameters.
        Example: {"image_0": ["identity", "translation", "scale"]} or {"image_0": ["affine"]}
    Returns
    -------
    list[BaseTransformation]
        A list of transformation objects corresponding to the specified transformations in the input.
    Notes    -----
    The function recognizes the following transformation types:
    - "identity": No transformation is applied.
    - "translation": A translation transformation with a fixed translation vector (e.g., [10, 20]).
    - "scale": A scaling transformation with fixed scale factors (e.g., [0.5, 0.5]).
    - "affine": An affine transformation with a fixed transformation matrix.
    If the input transformations are not specified, the function defaults to an identity transformation for the given key.  
    """

    if trans is None:
        return None

    coord_system = list(trans.keys())[0]
    trans = list(trans.items())[0][1]["transformations"]

    alltrans = []
    for tr in trans:
        if tr == "identity":
            tr = Identity()
        elif tr == "translation":
            tr = Translation([10, 20], axes = ("x", "y"))
        elif tr == "scale":
            tr = Scale([0.5, 0.5], axes = ("x", "y"))
        elif tr == "affine":
            tr = Affine(matrix = [
                    [0.5, 0.2, 0],
                    [0.1, 0.5, 0],
                    [0, 0, 1],
                ], 
                input_axes=("x", "y"), output_axes=("x", "y"))
        else:
            raise ValueError(f"Transformation type '{tr}' not recognized. Please choose from 'identity', 'translation', 'scale', or 'affine'.")
        alltrans.append(tr)
    
    if(len(alltrans) > 1):
        alltrans = Sequence(alltrans)
    elif len(alltrans) == 1:
        alltrans = alltrans[0]
    else:
        pass

    return {coord_system: alltrans}
    
def get_coordsystem_shape(
    coordinate_systems: Optional[dict] = None,
    coord_system: Optional[str] = None
) -> dict:
    if coordinate_systems is not None:
        if coord_system is not None:
            shape = coordinate_systems[coord_system]["shape"]
        else:
            shape = default_shape()   
    else:
        shape = default_shape()   
    return shape
        
def get_coordsystem_transformations(
    coordinate_systems: Optional[dict] = None
) -> dict:
    # transformations
    coord_systems = {}
    if coordinate_systems is not None:
        for i in coordinate_systems.keys():
            coord_systems.update(
                generate_transformations({i: coordinate_systems[i]})
            )
    return coord_systems

    