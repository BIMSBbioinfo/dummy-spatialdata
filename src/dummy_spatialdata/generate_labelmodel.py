import os
import sys
import numpy as np

from importlib.resources import files, as_file
from typing import Optional
from spatialdata.models import Labels2DModel
from spatialdata.transformations import set_transformation, Identity
from .generate_transformations import generate_transformations, get_basetransformations, get_shape
from .utils import default_shape

def generate_labelmodel(
    input: Optional[dict] = None,
    key: Optional[str] = None,
    coordinate_systems: Optional[dict] = None
) -> Labels2DModel:
    """Generate a dummy Labels2DModel object with specified elements.

    Parameters
    ----------
    input : int, optional
        A dictionary of key value pairs with 
            - n: number of labels, 
            - scale_factors: Scale factors to apply to construct a multiscale label/mask (datatree.DataTree). If None, a xarray.DataArray is returned instead. 
              Importantly, each scale factor is relative to the previous scale factor. For example, if the scale factors are [2, 2, 2], 
              the returned multiscale image will have 4 scales. The original image and then the 2x, 4x and 8x downsampled images and
            - coordinate_system: name of the coordinate_system (see 'coordinate_systems' parameter)
        Example: 
            {'n': 20, 'scale_factors': [2,2,2,2], 'coordinate_system': 'global'} # multi-scale
            {'n': 12, 'coordinate_system': 'global'} # single scale
    
    key: str
        the name of the element

    coordinate_systems: 
        A set of coordinate systems

    Returns
    -------
    Labels2DModel
        An Labels2DModel object populated with random data according to the specified parameters.
    """
    
    # return None if no input is provided
    if input is None:
        return None
    
    # get shape
    input.update(
        {'shape': get_shape(coordinate_systems, 
                            input['coordinate_system'] if 'coordinate_system' in input else None)}
    )

    # generate labels
    # mask for where values should be non-zero
    rows, cols = input['shape']['x'], input['shape']['y'],
    prob_nonzero = 0.1  # 5% non-zero values

    arr = np.zeros((rows, cols), dtype=int)
    mask = np.random.rand(rows, cols) < prob_nonzero
    arr[mask] = np.random.randint(1, input['n'], size=mask.sum())

    # get transformations
    coord_systems = get_basetransformations(coordinate_systems)
    if 'coordinate_system' in input:
        coord_system = input['coordinate_system']
        if coord_system in coord_systems:
            trans = {coord_system: coord_systems[coord_system]}
        else: 
            trans = {key: Identity()}
    else:
        trans = {key: Identity()}

    # image model
    if 'scale_factors' not in input:
        input["scale_factors"] = []
    labelmodel = Labels2DModel.parse(data=arr, 
                                     scale_factors=input['scale_factors'],
                                     transformations = trans)
        
    return labelmodel
    

    