import os
import sys
import numpy as np

from importlib.resources import files, as_file
from typing import Optional
from spatialdata.models import PointsModel
from spatialdata.transformations import set_transformation, Identity
import pandas as pd
from shapely.geometry import Point
from .generate_transformations import generate_transformations, get_basetransformations, get_shape
from .utils import default_shape

def generate_pointmodel(
    input: Optional[dict] = None,
    key: Optional[str] = None,
    coordinate_systems: dict = {},
    SEED: Optional[int] = 42
) -> PointsModel:
    """Generate a dummy PointsModel object with specified elements.

    Parameters
    ----------
    input : int, optional
        A dictionary of key value pairs with 
            - n: number of points, 
            - coordinate_system: name of the coordinate_system (see 'coordinate_systems' parameter)
        Example: 
            {'n': 12, 'coordinate_system': 'global'}
    
    key: str
        the name of the element

    coordinate_systems: 
        A set of coordinate systems

    SEED: int
        The seed value
        
    Returns
    -------
    PointsModel
        An PointsModel object populated with random data according to the specified parameters.
    """

    if input is None:
        return None

    # get shape
    # input.update(
    #     {'shape': get_shape(coordinate_systems, 
    #                        input['coordinate_system'] if 'coordinate_system' in input else None)}
    #)
    if 'shape' not in input:
        input.update({'shape': default_shape()})

    # generate points
    RADIUS = 0.08 * min(input['shape']['x'], input['shape']['y'])
    MIN_GAP = 0.01 * min(input['shape']['x'], input['shape']['y'])

    df = generate_points(input['shape']['x'], input['shape']['y'], input['n'], SEED)

    # get transformations
    coord_systems = get_basetransformations(coordinate_systems)
    if 'coordinate_system' in input:
        coord_system = input['coordinate_system']
        trans = {}
        for crd in coord_system:
            if crd in coord_systems:
                # trans = {crd: coord_systems[crd]}
                trans.update({crd: coord_systems[crd]})
            else: 
                trans = {key: Identity()}
    else:
        trans = {key: Identity()}

    # point model
    pointmodel = PointsModel.parse(df, transformations = trans)

    return pointmodel

def generate_points(width, height, n_points, SEED=1):
    rng = np.random.default_rng(SEED)
    
    df = pd.DataFrame({
        'x': rng.uniform(0, width, n_points),
        'y': rng.uniform(0, height, n_points)
    })
    
    return df