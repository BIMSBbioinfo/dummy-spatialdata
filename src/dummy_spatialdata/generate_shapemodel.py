import os
import sys
import numpy as np

from importlib.resources import files, as_file
from typing import Optional
from spatialdata.models import ShapesModel
from spatialdata.transformations import set_transformation, Identity
import geopandas as gpd
from shapely.geometry import Polygon
from .generate_transformations import generate_transformations, get_coordsystem_transformations, get_coordsystem_shape
from .utils import default_shape

def generate_shapemodel(
    input: Optional[dict] = None,
    key: Optional[str] = None,
    coordinate_systems: Optional[dict] = None,
    SEED: Optional[int] = 42
) -> ShapesModel:
    """Generate a dummy ShapesModel object with specified elements.

    Parameters
    ----------
    input : int, optional
        A dictionary of key value pairs with 
            - number of polygon shapes, 
            - name of the coordinate_system (see "coordinate_systems" parameter)
        Example: 
            [{"n_shapes": 12, "coordinate_system": "global"}]
    
    key: str
        the name of the element

    coordinate_systems: 
        A set of coordinate systems

    SEED: int
        The seed value

    Returns
    -------
    ShapesModel
        An ShapesModel object populated with random data according to the specified parameters.
    """

    if input is None:
        return None

    # get shape
    input.update(
        {"shape": get_coordsystem_shape(coordinate_systems, 
                                        input["coordinate_system"] if "coordinate_system" in input else None)}
    )

    # generate polygons
    RADIUS = 0.08 * min(input["shape"]["x"], input["shape"]["y"])
    MIN_GAP = 0.01 * min(input["shape"]["x"], input["shape"]["y"])

    centers = generate_non_overlapping_centers(input["shape"]["x"], input["shape"]["y"], RADIUS, input["n_shapes"], MIN_GAP, SEED)
    polygon_seeds = [SEED + i for i in range(input["n_shapes"])]
    polygons = [Polygon(border_polygon_points(c, RADIUS, 10, SEED = seed)) for c, seed in zip(centers, polygon_seeds)]
    gdf = gpd.GeoDataFrame(geometry=polygons)

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

    # shape model
    shapemodel = ShapesModel.parse(gdf, 
                                   transformations = trans)
    
    return shapemodel

def circles_overlap(c1, c2, radius, min_gap=0.0):
    x1, y1 = c1
    x2, y2 = c2
    return np.hypot(x2 - x1, y2 - y1) < (2 * radius + min_gap)

def generate_non_overlapping_centers(width, height, radius, n_circles, min_gap=0.15, SEED=1, max_tries=10000):
    centers = []
    tries = 0
    rng = np.random.default_rng(SEED)

    while len(centers) < n_circles and tries < max_tries:
        tries += 1
        x = rng.uniform(radius, width - radius)
        y = rng.uniform(radius, height - radius)
        candidate = (x, y)

        if all(not circles_overlap(candidate, c, radius, min_gap=min_gap) for c in centers):
            centers.append(candidate)

    if len(centers) < n_circles:
        raise RuntimeError(f"Could only place {len(centers)} circles after {max_tries} attempts.")

    return np.array(centers)

def border_polygon_points(center, radius, n_points, SEED=1):
    cx, cy = center
    rng = np.random.default_rng(SEED)

    # Random angles around the border
    angles = np.sort(rng.uniform(0, 2 * np.pi, n_points))

    # Points exactly on the circle border
    xs = cx + radius * np.cos(angles)
    ys = cy + radius * np.sin(angles)

    return np.column_stack([xs, ys])