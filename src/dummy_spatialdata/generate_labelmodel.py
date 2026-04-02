import os
import sys
import numpy as np

from importlib.resources import files, as_file
from typing import Optional
from spatialdata.models import Labels2DModel
from spatialdata.transformations import set_transformation, Identity
from .generate_transformations import generate_transformations, get_coordsystem_transformations, get_coordsystem_shape
from .utils import default_shape

def generate_labelmodel(
    input: Optional[dict] = None,
    key: Optional[str] = None,
    coordinate_systems: Optional[dict] = None
) -> Labels2DModel:
    
    # return None if no input is provided
    if input is None:
        return None
    
    # get shape
    input.update(
        {"shape": get_coordsystem_shape(coordinate_systems, 
                                        input["coordinate_system"] if "coordinate_system" in input else None)}
    )
    
    # generate labels
    # mask for where values should be non-zero
    rows, cols = input["shape"]["x"], input["shape"]["y"],
    prob_nonzero = 0.1  # 5% non-zero values

    arr = np.zeros((rows, cols), dtype=int)
    mask = np.random.rand(rows, cols) < prob_nonzero
    arr[mask] = np.random.randint(1, input["n_labels"], size=mask.sum())

    # get transformations
    coord_systems = get_coordsystem_transformations(coordinate_systems)
    if "coordinate_system" in input:
        coord_system = input["coordinate_system"]
        if coord_system in coord_systems:
            trans = {coord_system: coord_systems[coord_system]}
        else: 
            trans = {key: Identity()}
    else:
        trans = {key: Identity()}

    # image model
    labelmodel = Labels2DModel.parse(data=arr, 
                                     scale_factors=(2,) * (input["n_layers"]-1),
                                     transformations = trans)
        
    return labelmodel
    

    