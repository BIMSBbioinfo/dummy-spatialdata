import os
import sys
import numpy as np

from importlib.resources import files, as_file
from typing import Optional
from spatialdata.models import Labels2DModel
from spatialdata.transformations import set_transformation, Identity
from .generate_transformations import generate_transformations

def generate_labelmodel(
    input: Optional[dict] = None,
    key: Optional[str] = None
) -> Labels2DModel:
    
    # return None if no input is provided
    if input is None:
        return None
    
    # generate labels
    # mask for where values should be non-zero
    rows, cols = input["shape"]["x"], input["shape"]["y"],
    prob_nonzero = 0.1  # 5% non-zero values

    arr = np.zeros((rows, cols), dtype=int)
    mask = np.random.rand(rows, cols) < prob_nonzero
    arr[mask] = np.random.randint(1, input["n_labels"], size=mask.sum())

    # image model
    labelmodel = Labels2DModel.parse(data=arr, 
                                     scale_factors=(2,) * (input["n_layers"]-1),
                                    transformations = {key: Identity()})

    # generate transformations
    if "transformations" in input:
        trans =  generate_transformations(input["transformations"])    
        for x in trans.keys():
            set_transformation(labelmodel,
                               transformation = trans[x], to_coordinate_system = x)
        
    return labelmodel
    

    