import os
import sys
import numpy as np

from importlib.resources import files, as_file
from typing import Optional
from spatialdata.models import PointsModel
from spatialdata.transformations import set_transformation, Identity
import pandas as pd
from shapely.geometry import Point
from .generate_transformations import generate_transformations

def generate_pointmodel(
    input: Optional[dict] = None,
    key: Optional[str] = None,
    transformations: Optional[dict] = None,
    SEED: Optional[int] = 42
) -> pd.DataFrame:

    if input is None:
        return None

    # generate points
    RADIUS = 0.08 * min(input["shape"]["x"], input["shape"]["y"])
    MIN_GAP = 0.01 * min(input["shape"]["x"], input["shape"]["y"])

    df = generate_points(input["shape"]["x"], input["shape"]["y"], input["n_points"], SEED)

    # get transformations
    if "transformations" in input:
        if input["transformations"] in transformations:
            trans = {input["transformations"]: transformations[input["transformations"]]}
        else: 
            trans = {key: Identity()}
    else:
        trans = {key: Identity()}

    # point model
    pointmodel = PointsModel.parse(df, 
                                   transformations = trans)

    return pointmodel

def generate_points(width, height, n_points, SEED=1):
    rng = np.random.default_rng(SEED)
    
    df = pd.DataFrame({
        "x": rng.uniform(0, width, n_points),
        "y": rng.uniform(0, height, n_points)
    })
    
    return df